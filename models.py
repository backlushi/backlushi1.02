core/models.py
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=True)
    calories = Column(Float, nullable=True)
    shelf_life_days = Column(Integer, nullable=True)  # Можно не учитывать
    category = Column(String, nullable=True)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, brand={self.brand})>"

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False, default=0)
    unit = Column(String, nullable=False, default="шт")  # штуки, кг, л, и т.д.
    user_id = Column(Integer, nullable=False)  # Если нужна мультипользовательская система

    product = relationship("Product")

    def __repr__(self):
        return f"<InventoryItem(id={self.id}, product={self.product.name}, qty={self.quantity}{self.unit})>"

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    preferred_brands = Column(String, nullable=True)  # например, JSON строка с брендами

    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id}, preferred_brands={self.preferred_brands})>"
