from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    url = Column(String(255), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"))  # Relación con Store

    # Relación ORM (opcional si luego agregas Store)
    store = relationship("Store", back_populates="products")