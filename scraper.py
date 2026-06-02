import httpx
from bs4 import BeautifulSoup
import logging

log = logging.getLogger(__name__)

# En-têtes réalistes pour éviter d'être bloqué
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xhtml+xml;q=0.9,*/*;q=0.8',
}

# Mots-clés d'indisponibilité par défaut (FR + EN)
DEFAULT_UNAVAILABLE_KEYWORDS = [
    'rupture de stock', 'rupture', 'indisponible', 'épuisé',
    'out of stock', 'sold out', 'unavailable', 'hors stock',
    'temporairement indisponible', 'plus disponible',
]


async def check_product(product: dict) -> bool:
    """
    Vérifie si un produit est disponible.
    Retourne True si disponible, False sinon.

    Méthodes de détection (dans products.json) :
    1. 'selector' + optionnel 'unavailable_keywords' → sélecteur CSS ciblant un élément
    2. 'unavailable_text' → le texte indique que c'est indisponible
    3. 'available_text'   → le texte indique que c'est disponible
    """
    try:
        async with httpx.AsyncClient(
            headers=HEADERS, timeout=20, follow_redirects=True
        ) as client:
            response = await client.get(product['url'])
            response.raise_for_status()

       soup = BeautifulSoup(response.text, 'html.parser')

        # --- Méthode 1 : sélecteur CSS ---
        if 'selector' in product:
            element = soup.select_one(product['selector'])
            if element is None:
                log.debug(f"Sélecteur '{product['selector']}' introuvable sur {product['name']}")
                return False
            text = element.get_text(strip=True).lower()
            keywords = product.get('unavailable_keywords', DEFAULT_UNAVAILABLE_KEYWORDS)
            return not any(kw.lower() in text for kw in keywords)

        # --- Méthode 2 : texte d'indisponibilité ---
        if 'unavailable_text' in product:
            return product['unavailable_text'].lower() not in response.text.lower()

        # --- Méthode 3 : texte de disponibilité ---
        if 'available_text' in product:
            return product['available_text'].lower() in response.text.lower()

        log.warning(
            f"Aucune méthode configurée pour {product['name']}. "
            "Ajoute 'selector', 'unavailable_text' ou 'available_text' dans products.json"
        )
        return False

    except httpx.HTTPStatusError as e:
        log.error(f"Erreur HTTP {e.response.status_code} pour {product['name']}")
        return False
    except httpx.TimeoutException:
        log.error(f"Timeout pour {product['name']}")
        return False
    except Exception as e:
        log.error(f"Erreur scraping {product['name']} : {e}")
        return False
