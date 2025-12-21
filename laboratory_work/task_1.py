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





