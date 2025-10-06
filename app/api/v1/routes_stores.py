from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreRead

router = APIRouter(prefix="/stores", tags=["Stores"])

@router.post("/", response_model=StoreRead)
async def create_store(store: StoreCreate, db: AsyncSession = Depends(get_db)):
    new_store = Store(**store.model_dump())
    db.add(new_store)
    await db.commit()
    await db.refresh(new_store)
    return new_store

@router.get("/", response_model=list[StoreRead])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Store))
    products = result.scalars().all()
    return products