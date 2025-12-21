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

    @classmethod
    def save_recipes(cls, filename: str = 'recipes.json'):
        """Сохранение рецептов в JSON файл"""

        data = []
        for recipe in cls._recipes.values():
            recipe_data = asdict(recipe)
            recipe_data['toppings'] = [asdict(t) for t in recipe.toppings]
            data.append(recipe_data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def get_recipe(cls, name: str):
        """Возврат рецепта по имени"""

        return cls._recipes.get(name)

    @classmethod
    def get_all_recipes(cls):
        """Список всех доступных рецептов"""

        return list(cls._recipes.values())

    @classmethod
    def create_custom_recipe(cls, name: str, base_price: float, base_cost: float,
                             toppings: List[Topping], description: str = ""):
        """Создание и сохранение нового пользовательского рецепта"""

        recipe = PizzaRecipe(name, base_price, base_cost, toppings, description)
        cls._recipes[name] = recipe
        return recipe

    @classmethod
    def delete_recipe(cls, name: str):
        """Удаление рецепта по имени"""

        if name in cls._recipes:
            del cls._recipes[name]

class Order:
    """Класс, представляющий заказ на пиццу"""

    _next_id = 1
    def __init__(self, pizza: Pizza, price_strategy: PriceStrategy = None):
        self.order_id = Order._next_id
        Order._next_id += 1
        self.pizza = pizza
        self.price_strategy = price_strategy or StandardPriceStrategy()
        self.order_date = datetime.datetime.now()
        self._observers: List[OrderObserver] = []

    @property
    def total_price(self):
        """Расчет общей стоимости заказа"""
        return self.pizza.get_total_price(self.price_strategy)

    @property
    def total_cost(self):
        """Расчет общей себестоимости заказа"""
        return self.pizza.get_total_cost()

    @property
    def profit(self):
        """Расчет прибыли от заказа"""
        return self.total_price - self.total_cost

    def add_observer(self, observer: OrderObserver):
        """Добавление наблюдения к заказу"""
        self._observers.append(observer)

    def notify_observer(self):
        """Уведомляет о создании заказа"""
        for observer in self._observers:
            observer.update(self)

    def save_to_file(self, filename: str = 'order.json'):
        """Сохранение информации о заказе в JSON файл"""

        order_data = {
            'order_id': self.order_id,
            'pizza_name': self.pizza.name,
            'total_price': self.total_price,
            'total_cost': self.total_cost,
            'profit': self.profit,
            'order_date': self.order_date.isoformat(),
            'toppings': [t.name for t in self.pizza.all_toppings]
        }

        orders = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                orders = json.load(f)

        orders.append(order_data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)



