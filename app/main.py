from fastapi import FastAPI
from app.api.v1.routes_products import router as product_router
from app.api.v1.routes_stores import router as store_router
from app.api.v1.routes_scraper import router as scraper_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Registrar el router de productos
app.include_router(product_router, tags=["Products"])
app.include_router(store_router)
app.include_router(scraper_router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}!"}