import asyncio
from app.db.session import engine, Base
from app.models import product, store  # 👈 importa tus modelos

async def init_models():
    async with engine.begin() as conn:
        print("Creando tablas en la base de datos...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tablas creadas correctamente.")

if __name__ == "__main__":
    asyncio.run(init_models())
