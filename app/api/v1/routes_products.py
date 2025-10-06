from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.product import Product
from app.models.store import Store
from app.schemas.product import ProductCreate, ProductRead
from typing import Optional

router = APIRouter(prefix="/products", tags=["Products"])

# Crear producto
@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si la tienda existe
    result = await db.execute(select(Store).where(Store.id == product.store_id))
    store = result.scalar_one_or_none()

    if store is None:
        raise HTTPException(status_code=404, detail="La tienda no existe")

    # Validar que el precio sea positivo
    if product.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio debe ser mayor que cero."
        )

    # Verificar si ya existe un producto con el mismo URL
    existing_product_query = await db.execute(
        select(Product).where(
            (Product.url == product.url)
        )
    )
    existing_product = existing_product_query.scalar_one_or_none()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un producto con ese URL."
        )

    # Crear el producto
    new_product = Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


# Listar productos (con filtro opcional por tienda)
@router.get("/", response_model=list[ProductRead])
async def get_products(store_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Product)

    # Si se pasa el parámetro store_id, filtramos
    if store_id is not None:
        query = query.where(Product.store_id == store_id)

    result = await db.execute(query)
    products = result.scalars().all()

    if not products:
        raise HTTPException(status_code=404, detail="No se encontraron productos")

    return products


# Obtener producto por ID
@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product