from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.store import Store
import random
import asyncio
from sqlalchemy.future import select

@celery_app.task(bind=True, name="app.tasks.scraper.simulate_scraping")
def simulate_scraping(self, product_name: str):
    """
    Tarea que obtiene las tiendas desde la base de datos y simula scraping de precios.
    """

    async def run_scraping():
        async with AsyncSessionLocal() as session:
            # Usa select(Store) para obtener objetos del ORM
            result = await session.execute(select(Store))
            stores = result.scalars().all()

        results = []
        total = len(stores)
        for i, store in enumerate(stores, start=1):
            # Simula latencia y precio
            await asyncio.sleep(1)
            results.append({
                "store": store.name,
                "product": product_name,
                "price": round(random.uniform(100, 1000), 2)
            })
            # Actualiza estado de progreso
            self.update_state(state="PROGRESS", meta={"progress": f"{i}/{total}"})
        
        return results

    # Ejecuta la corrutina
    return asyncio.run(run_scraping())
