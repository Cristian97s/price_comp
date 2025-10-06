from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductRead
from typing import Optional

router = APIRouter(prefix="/scraper", tags=["Scraper"])

@router.get("/", response_model=list[ProductRead])
async def get_scraping(name_product: Optional[str] = Query(None, description="Nombre o parte del nombre del producto"), db: AsyncSession = Depends(get_db)):
    query = select(Product)

    if name_product is not None:
        query = query.where(Product.name.ilike(f"%{name_product}%"))

    result = await db.execute(query)
    products = result.scalars().all()

    if not products:
        raise HTTPException(status_code=404, detail="No se encontraron productos")
    
    return products