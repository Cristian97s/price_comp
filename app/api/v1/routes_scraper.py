from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductRead
from app.tasks.scraper import simulate_scraping
from app.core.celery_app import celery_app
from typing import Optional

router = APIRouter(prefix="/scraper", tags=["Scraper"])

@router.get("/", response_model=list[ProductRead])
async def get_scraping(name_product: Optional[str] = Query(None, description="Nombre o parte del nombre del producto"),db: AsyncSession = Depends(get_db)):
    query = select(Product)

    if name_product:
        query = query.where(Product.name.ilike(f"%{name_product}%"))

    result = await db.execute(query)
    products = result.scalars().all()

    if not products:
        raise HTTPException(status_code=404, detail="No se encontraron productos")
    
    return products

@router.get("/run")
async def run_scraper(product_name: str):
    task = simulate_scraping.delay(product_name)
    return {"task_id": task.id, "status": "Scraping iniciado"}

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    response = {
        "task_id": task.id,
        "status": task.status,
    }

    # Si la tarea tiene información adicional (meta)
    if isinstance(task.info, dict):
        response.update(task.info)
    elif isinstance(task.info, Exception):
        response["error"] = str(task.info)

    # Si la tarea terminó, agrega el resultado final
    if task.ready():
        response["result"] = task.result

    return response