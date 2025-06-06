from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    category = Column(String, nullable=True)
    calories = Column(Float, nullable=True)
    shelf_life_days = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Product(name='{self.name}', brand='{self.brand}')>"

class InventoryItem(Base):
    __tablename__ = 'inventory_items'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    expiration_date = Column(Date, nullable=True)  # Лучше использовать Date, а не String

    product = relationship("Product")

    def __repr__(self):
        return f"<InventoryItem(product='{self.product.name}', quantity={self.quantity})>"