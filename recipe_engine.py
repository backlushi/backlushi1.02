from core.services import CoreService
from typing import List, Dict, Any


class RecipeEngine:
    def __init__(self, core_service: CoreService):
        self.core_service = core_service

    def filter_recipes_by_inventory(self, user_id: int, recipes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Отфильтровать рецепты, оставив только те, у которых все ингредиенты есть в инвентаре
        на нужное количество. Учитываем только наличие продуктов, без сложной логики по срокам.
        """
        inventory = self.core_service.get_inventory_for_user(user_id)
        inv_map = {item.product.name.lower(): item.quantity for item in inventory}

        filtered = []
        for recipe in recipes:
            if self._can_make_recipe(recipe, inv_map):
                filtered.append(recipe)
        return filtered

    def _can_make_recipe(self, recipe: Dict[str, Any], inv_map: Dict[str, float]) -> bool:
        for ingredient in recipe.get("ingredients", []):
            name = ingredient["name"].lower()
            required_qty = ingredient.get("quantity", 1)
            if inv_map.get(name, 0) < required_qty:
                return False
        return True

    def rank_recipes_by_preferences(self, user_id: int, recipes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Простое ранжирование по брендам из пользовательских предпочтений.
        Чем больше совпадений, тем выше рейтинг.
        """
        prefs = self.core_service.get_user_preferences(user_id)
        if not prefs or not prefs.preferred_brands:
            return recipes  # Нет предпочтений — возвращаем без изменений

        preferred_brands = set(brand.strip().lower() for brand in prefs.preferred_brands.split(","))

        def score(recipe):
            score = 0
            for ingredient in recipe.get("ingredients", []):
                brand = ingredient.get("brand", "").lower()
                if brand in preferred_brands:
                    score += 1
            return score

        return sorted(recipes, key=score, reverse=True)

    def suggest_recipes(self, user_id: int, recipes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Основной метод — фильтрация и сортировка рецептов по наличию и предпочтениям.
        """
        filtered = self.filter_recipes_by_inventory(user_id, recipes)
        ranked = self.rank_recipes_by_preferences(user_id, filtered)
        return ranked


чек
валидатор


class CheckValidator:
    def validate(self, raw_check: dict) -> bool:
        # Проверка ключевых полей, формата, целостности данных
        pass


class BrandNormalizer:
    def normalize(self, brand_name: str) -> str:
        # Приведение к каноническому виду, проверка в словаре
        pass


class CheckParser:
    def parse(self, raw_check: str) -> dict:
        # Парсинг с поддержкой нескольких форматов
        pass


class CheckImporter:
    def __init__(self, validator: CheckValidator, normalizer: BrandNormalizer, preferences_module):
        # Инициализация с зависимостями
        pass

    def import_check(self, raw_check: str):
        # Полный цикл: валидация, парсинг, нормализация, обновление предпочтений
        pass


архитектура
импорта
чеков
from abc import ABC, abstractmethod


class BaseCheckParser(ABC):
    @abstractmethod
    def parse(self, raw_data: str) -> dict:
        """
        Парсинг сырых данных чека в унифицированный формат
        """
        pass


class VkusVillParser(BaseCheckParser):
    def parse(self, raw_data: str) -> dict:
        # Логика парсинга именно чеков ВкусВилл
        pass


class CheckParserFactory:
    parsers = {
        'vkusvill': VkusVillParser,
        # можно добавить новых
    }

    @staticmethod
    def get_parser(store_name: str) -> BaseCheckParser:
        parser_cls = CheckParserFactory.parsers.get(store_name)
        if not parser_cls:
            raise ValueError(f"No parser for store {store_name}")
        return parser_cls()


class CheckImporter:
    def __init__(self, store_name: str):
        self.parser = CheckParserFactory.get_parser(store_name)

    def import_check(self, raw_data: str):
        standard_check = self.parser.parse(raw_data)
        # Далее валидация, нормализация, обновление предпочтений
        pass