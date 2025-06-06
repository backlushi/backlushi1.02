import json
from collections import defaultdict
from typing import Dict, List, Optional


class UserPreferences:
    def __init__(self):
        # category -> { brand_name: count }
        self.brand_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def add_purchase(self, category: str, brand: str, count: int = 1):
        """Добавляет бренд в статистику по категории"""
        self.brand_stats[category][brand] += count

    def get_top_brands(self, category: str, top_n: int = 3) -> List[str]:
        """Возвращает список наиболее частых брендов в категории"""
        if category not in self.brand_stats:
            return []
        sorted_brands = sorted(self.brand_stats[category].items(), key=lambda x: -x[1])
        return [brand for brand, _ in sorted_brands[:top_n]]

    def load_from_file(self, filepath: str):
        """Загружает предпочтения из JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for category, brand_counts in data.items():
                    self.brand_stats[category] = defaultdict(int, brand_counts)
        except FileNotFoundError:
            print(f"[INFO] Файл {filepath} не найден. Начинаем с пустых предпочтений.")
        except Exception as e:
            print(f"[ERROR] Ошибка загрузки предпочтений: {e}")

    def save_to_file(self, filepath: str):
        """Сохраняет предпочтения в JSON"""
        data = {cat: dict(brand_counts) for cat, brand_counts in self.brand_stats.items()}
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[ERROR] Ошибка сохранения предпочтений: {e}")

    def __str__(self):
        return json.dumps({k: dict(v) for k, v in self.brand_stats.items()}, indent=2, ensure_ascii=False)