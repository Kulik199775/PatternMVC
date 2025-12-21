import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum
import datetime
import os

# Паттерн стратегия

class PriceStrategy(ABC):
    """Абстрактный класс стратегии для расчета цены"""

    @abstractmethod
    def calculate_price(self, base_price: float):
        """Расчитывает итоговую цену на основе базовой"""
        pass

class StandardPriceStrategy(PriceStrategy):
    """Стандартная цена (без изменений)"""
    def calculate_price(self, base_price: float):
        return base_price

class DiscountPriceStrategy(PriceStrategy):
    """Цена со скидкой"""

    def __init__(self, discount_percent: float):
        self.discount = discount_percent / 100

    def calculate_price(self, base_price: float):
        """Расчет цены со скидкой"""
        return base_price * (1 - self.discount)

class OrderObserver(ABC):
    """Абстрактный класс - наблюдение за заказами"""

    @abstractmethod
    def update(self, order: 'Order'):
        """Метод, вызываемый при изменении состояния заказа"""
        pass

class OrderLogger(OrderObserver):
    """Класс для логирования создания заказов"""

    def update(self, order: 'Order'):
        """Логирует информация о созданном заказе"""
        print(f'Заказ #{order.order_id} создан: {order.pizza.name}')

class StatisticsTracker(OrderObserver):
    """Класс для отслеживания статистики продаж"""

    def __init__(self):
        self.total_orders = 0
        self.total_revenue = 0.0

    def update(self, order: 'Order'):
        self.total_orders += 1
        self.total_revenue += order.total_price

@dataclass
class Topping:
    """Класс для представления ингредиентов пиццы"""

    name: str
    price: float
    cost: float

@dataclass
class PizzaRecipe:
    """Класс для представления рецепта пиццы"""

    name: str
    base_price: float
    base_cost: float
    toppings: List[Topping]
    description: str = ""

class Pizza:
    """Класс для представления приготовленной пиццы по рецепту"""

    def __init__(self, recipe: PizzaRecipe, custom_toppings: List[Topping] = None):
        self.recipe = recipe
        self.custom_toppings = custom_toppings or []

    @property
    def name(self):
        """Название пиццы"""
        return self.recipe.name

    @property
    def all_toppings(self):
        """Все начинки для пиццы"""
        return self.recipe.toppings + self.custom_toppings

    @property
    def base_price(self):
        """Базовая пицца из рецепта"""
        return self.recipe.base_price

    @property
    def base_cost(self):
        """Базовая себестоимость пиццы из рецепта"""
        return self.recipe.base_cost

    def get_total_cost(self):
        """Полная себестоимость пиццы"""
        toppings_cost = sum(t.cost for t in self.all_toppings)
        return self.base_cost + toppings_cost

    def get_total_price(self, strategy: PriceStrategy = None):
        """Полная цена пиццы с учетом ценообразования"""

        if strategy is None:
            strategy = StandardPriceStrategy()

        toppings_price = sum(t.price for t in self.all_toppings)
        base_price = self.base_price + toppings_price
        return strategy.calculate_price(base_price)

class PizzaFactory:
    """Паттерн фабрика - для создания пицц"""
    _recipes: Dict[str, PizzaRecipe] = {}

    @classmethod
    def load_recipes(cls, filename: str = 'recipes.json'):
        """Загрузка рецептов из JSON файла"""

        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for recipe_data in data:
                    toppings = [Topping(**t) for t in recipe_data['toppings']]
                    recipe = PizzaRecipe(
                        name=recipe_data['name'],
                        base_price=recipe_data['base_price'],
                        base_cost=recipe_data['base_cost'],
                        toppings=toppings,
                        description=recipe_data.get('description', '')
                    )
                    cls._recipes[recipe.name] = recipe






