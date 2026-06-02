import httpx
from bs4 import BeautifulSoup
import logging

log = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xhtml+xml;q=0.9,*/*;q=0.8',
}

DEFAULT_UNAVAILABLE_KEYWORDS = [
    'rupture de stock', 'rupture', 'indisponible', 'épuisé',
    'out of stock', 'sold out', 'unavailable', 'hors stock',
    'temporairement indisponible', 'plus disponible',
]


async def check_product(product: dict) -> bool:
    try:
        async with httpx.AsyncClient(
            headers=HEADERS, timeout=20, follow_redirects=True
        ) as client:
            response = await client.get(product['url'])
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        if 'selector' in product:
            element = soup.select_one(product['selector'])
            if element is None:
                return False
            text = element.get_text(strip=True).lower()
            keywords = product.get('unavailable_keywords', DEFAULT_UNAVAILABLE_KEYWORDS)
            return not any(kw.lower() in text for kw in keywords)

        if 'unavailable_text' in product:
            return product['unavailable_text'].lower() not in response.text.lower()

        if 'available_text' in product:
            return product['available_text'].lower() in response.text.lower()

        log.warning(f"Aucune méthode configurée pour {product['name']}")
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
