from core.dao import Dao
from core.models import Product, InventoryItem, UserPreference

class CoreService:
    def __init__(self, dao: Dao):
        self.dao = dao

    # Продукты

    def create_product(self, name: str, brand: str | None = None,
                       calories: float | None = None, shelf_life_days: int | None = None,
                       category: str | None = None) -> Product:
        product = Product(name=name, brand=brand, calories=calories,
                          shelf_life_days=shelf_life_days, category=category)
        return self.dao.add_product(product)

    def list_products(self, limit: int = 100) -> list[Product]:
        return self.dao.list_products(limit)

    # Инвентарь

    def add_inventory_item(self, user_id: int, product_id: int,
                           quantity: float, unit: str = "шт") -> InventoryItem:
        item = InventoryItem(user_id=user_id, product_id=product_id,
                             quantity=quantity, unit=unit)
        return self.dao.add_inventory_item(item)

    def update_inventory_quantity(self, item_id: int, new_quantity: float) -> InventoryItem | None:
        return self.dao.update_inventory_item_quantity(item_id, new_quantity)

    def get_inventory_for_user(self, user_id: int) -> list[InventoryItem]:
        return self.dao.get_inventory_for_user(user_id)

    # Предпочтения

    def get_user_preferences(self, user_id: int) -> UserPreference | None:
        return self.dao.get_user_preferences(user_id)

    def set_user_preferences(self, user_id: int, preferred_brands: str) -> UserPreference:
        pref = UserPreference(user_id=user_id, preferred_brands=preferred_brands)
        return self.dao.set_user_preferences(pref)


подкючение к базе пример запуска
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base
from core.dao import Dao
from core.services import CoreService

DATABASE_URL = "sqlite:///./product_db.sqlite"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_service() -> CoreService:
    session = SessionLocal()
    dao = Dao(session)
    return CoreService(dao)

if __name__ == "__main__":
    init_db()
    service = get_service()

    # Демка
    p = service.create_product(name="Молоко", brand="ВкусВилл", calories=60, shelf_life_days=7, category="Молочные")
    print(f"Created product: {p}")

    items = service.list_products()
    print(f"Products: {items}")

