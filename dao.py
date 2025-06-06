from sqlalchemy.orm import Session
from core.models import Product, InventoryItem, UserPreference

class Dao:
    def __init__(self, session: Session):
        self.session = session

    # --- Products ---

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.session.query(Product).filter(Product.id == product_id).first()

    def add_product(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        return product

    def list_products(self, limit: int = 100) -> list[Product]:
        return self.session.query(Product).limit(limit).all()

    # --- Inventory ---

    def get_inventory_for_user(self, user_id: int) -> list[InventoryItem]:
        return self.session.query(InventoryItem).filter(InventoryItem.user_id == user_id).all()

    def add_inventory_item(self, item: InventoryItem) -> InventoryItem:
        self.session.add(item)
        self.session.commit()
        return item

    def update_inventory_item_quantity(self, item_id: int, new_qty: float) -> InventoryItem | None:
        item = self.session.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if item:
            item.quantity = new_qty
            self.session.commit()
        return item

    # --- Preferences ---

    def get_user_preferences(self, user_id: int) -> UserPreference | None:
        return self.session.query(UserPreference).filter(UserPreference.user_id == user_id).first()

    def set_user_preferences(self, pref: UserPreference) -> UserPreference:
        existing = self.get_user_preferences(pref.user_id)
        if existing:
            existing.preferred_brands = pref.preferred_brands
        else:
            self.session.add(pref)
        self.session.commit()
        return pref
