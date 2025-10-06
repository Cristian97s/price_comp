from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base 
from app.core.config import settings

# Crear el motor de conexión
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Crear sesión asíncrona
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Declarative Base para los modelos
Base = declarative_base()

# Dependencia para usar en endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session