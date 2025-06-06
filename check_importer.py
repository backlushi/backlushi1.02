# Импорт чеков из магазинов
import json
from core.preferences import UserPreferences


class CheckImporter:
    def __init__(self, preferences: UserPreferences, brand_map=None, category_map=None):
        """
        brand_map: словарь product_name -> brand
        category_map: словарь product_name -> category
        """
        self.preferences = preferences
        self.brand_map = brand_map or {}
        self.category_map = category_map or {}

    def parse_check(self, filepath: str):
        """
        Парсит простой JSON-чек формата:
        [
            { "product": "Молоко Простоквашино 3.2%", "quantity": 1 },
            { "product": "Хлеб нарезной Хлебозавод №12", "quantity": 2 }
        ]
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                check_items = json.load(f)
        except Exception as e:
            print(f"[ERROR] Ошибка загрузки чека: {e}")
            return

        for item in check_items:
            name = item['product']
            quantity = item.get('quantity', 1)

            brand = self._extract_brand(name)
            category = self._extract_category(name)

            if brand and category:
                self.preferences.add_purchase(category, brand, quantity)
            else:
                print(f"[WARN] Не удалось определить категорию/бренд для: {name}")

    def _extract_brand(self, product_name: str) -> str:
        return self.brand_map.get(product_name, self._guess_brand(product_name))

    def _extract_category(self, product_name: str) -> str:
        return self.category_map.get(product_name, self._guess_category(product_name))

    def _guess_brand(self, product_name: str) -> str:
        # На будущее: NLP или regexp
        words = product_name.split()
        return words[1] if len(words) > 1 else "UNKNOWN"

    def _guess_category(self, product_name: str) -> str:
        # Можно заменить на ML-модель или таблицу соответствия
        if "молоко" in product_name.lower():
            return "milk"
        elif "хлеб" in product_name.lower():
            return "bread"
        else:
            return "other"
