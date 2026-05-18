import asyncio
import json
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scraper import check_product
from notifier import send_telegram
from database import init_db, get_status, set_status

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)


def load_products():
    with open('products.json', 'r', encoding='utf-8') as f:
        return json.load(f)


async def check_all_products():
    products = load_products()
    log.info(f"🔍 Vérification de {len(products)} produit(s)...")

    for product in products:
        try:
            is_available = await check_product(product)
            previous = get_status(product['id'])

            if is_available and not previous:
                # Nouveau : produit passé à disponible → alerte !
                log.info(f"✅ DISPONIBLE : {product['name']}")
                await send_telegram(
                    f"✅ *{product['name']}* est disponible !\n\n"
                    f"🔗 [Voir le produit]({product['url']})"
                )
                set_status(product['id'], True)

            elif not is_available and previous:
                # Produit redevenu indisponible → on met à jour silencieusement
                log.info(f"❌ De nouveau indisponible : {product['name']}")
                set_status(product['id'], False)

            else:
                status = "disponible" if is_available else "indisponible"
                log.info(f"⏸  Pas de changement : {product['name']} ({status})")

        except Exception as e:
            log.error(f"Erreur pour {product['name']} : {e}")


async def main():
    init_db()
    log.info("🤖 Bot démarré — vérification toutes les 10 minutes")

    # Vérification immédiate au démarrage
    await check_all_products()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_all_products, 'interval', minutes=10)
    scheduler.start()

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        log.info("Bot arrêté proprement.")


if __name__ == '__main__':
    asyncio.run(main())
