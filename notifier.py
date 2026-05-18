import httpx
import os
import logging

log = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')


async def send_telegram(message: str) -> bool:
    """
    Envoie un message Telegram via l'API Bot.
    Retourne True si succès, False sinon.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        log.error(
            "❌ Variables manquantes : TELEGRAM_TOKEN et TELEGRAM_CHAT_ID "
            "doivent être définis en variables d'environnement."
        )
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': False,
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            log.info("📨 Notification Telegram envoyée avec succès")
            return True
    except httpx.HTTPStatusError as e:
        log.error(f"Erreur API Telegram ({e.response.status_code}) : {e.response.text}")
        return False
    except Exception as e:
        log.error(f"Erreur envoi Telegram : {e}")
        return False


async def send_startup_message():
    """Envoie un message de confirmation au démarrage du bot."""
    await send_telegram(
        "🤖 *Bot de surveillance démarré !*\n"
        "Je vérifierai les stocks toutes les 10 minutes et t'alerterai dès qu'un produit est disponible."
    )
