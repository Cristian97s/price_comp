from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.product import Product
from app.scrapers.scraper_001 import scrape_store_001
import asyncio

@celery_app.task(bind=True, name="app.tasks.scraper.real_scraping")
def real_scraping(self, product_name: str):
    async def run_scraping():
        scrapers = [scrape_store_001]  # luego agregamos mas tiendas
        results = []

        async with AsyncSessionLocal() as session:
            total = len(scrapers)
            for i, scraper in enumerate(scrapers, start=1):
                try:
                    data = await scraper(product_name, session)
                    results.extend(data)
                    # Guardar productos en DB
                    for item in data:
                        product = Product(
                            name=item["name"],
                            price=item["price"],
                            url=item["url"],
                            store_id=item["store_id"]
                        )
                        session.add(product)
                    await session.commit()
                    self.update_state(state="PROGRESS", meta={"progress": f"{i}/{total}"})
                except Exception as e:
                    print(f"Error en {scraper.__name__}: {e}")

        return results

    return asyncio.run(run_scraping())
