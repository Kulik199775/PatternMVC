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

class OrderManager:
    """Управление заказами"""

    def __init__(self):
        self.orders: List[Order] = []
        self.statistics = StatisticsTracker()

    def create_order(self, pizza: Pizza, price_strategy: PriceStrategy = None):
        """Создание и регистрация заказа в системе"""

        order = Order(pizza, price_strategy)
        order.add_observer(self.statistics)
        order.add_observer(OrderLogger())
        order.notify_observer()
        order.save_to_file()
        self.orders.append(order)
        return order

    def get_total_statistics(self):
        """Общая статистика по всем заказам"""

        total_revenue = sum(o.total_price for o in self.orders)
        total_cost = sum(o.total_cost for o in self.orders)
        total_profit = total_revenue - total_cost

        return {
            'total_orders': len(self.orders),
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'total_profit': total_profit
        }


class UserInterface:
    """Основной пользовательский интерфейс приложения"""

    def __init__(self):
        """Инициализирует пользовательский интерфейс"""

        self.order_manager = OrderManager()
        self.available_toppings = [
            Topping("Сыр", 50, 20),
            Topping("Ветчина", 70, 30),
            Topping("Грибы", 40, 15),
            Topping("Пепперони", 60, 25),
            Topping("Оливки", 30, 10),
            Topping("Помидоры", 25, 8),
            Topping("Лук", 20, 5),
            Topping("Перец", 30, 12)
        ]

        self._load_standard_recipes()

    def _load_standard_recipes(self):
        """Загружает стандартные рецепты пицц в фабрику"""
        standard_recipes = [
            PizzaRecipe(
                name="Маргарита",
                base_price=300,
                base_cost=100,
                toppings=[self.available_toppings[0]],  # Сыр
                description="Классическая пицца с томатным соусом и сыром"
            ),
            PizzaRecipe(
                name="Пепперони",
                base_price=400,
                base_cost=150,
                toppings=[self.available_toppings[0], self.available_toppings[3]],
                description="Острая пицца с пепперони и сыром"
            ),
            PizzaRecipe(
                name="Гавайская",
                base_price=450,
                base_cost=160,
                toppings=[self.available_toppings[0], self.available_toppings[1]],
                description="С ветчиной и ананасами"
            ),
            PizzaRecipe(
                name="Четыре сыра",
                base_price=500,
                base_cost=180,
                toppings=[self.available_toppings[0]],
                description="Смесь четырех разных сыров"
            ),
            PizzaRecipe(
                name="Вегетарианская",
                base_price=350,
                base_cost=120,
                toppings=[self.available_toppings[2], self.available_toppings[5], self.available_toppings[6]],
                description="Свежие овощи на тонком тесте"
            )
        ]

        for recipe in standard_recipes:
            PizzaFactory._recipes[recipe.name] = recipe

    def show_main_menu(self):
        """Отображает главное меню приложения и обрабатывает выбор пользователя"""
        while True:
            print("\nДобро пожаловать в пиццерию!")
            print("1. Сделать заказ")
            print("2. Просмотреть статистику")
            print("3. Админ-панель")
            print("4. Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.make_order()
            elif choice == "2":
                self.show_statistics()
            elif choice == "3":
                self.admin_panel()
            elif choice == "4":
                print("До свидания!")
                break
            else:
                print("Неверный выбор!")

    def make_order(self):
        """Процесс создания нового заказа"""
        print("\nСоздание заказа")

        recipes = PizzaFactory.get_all_recipes()
        print("\nДоступные рецепты:")
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe.name} - {recipe.base_price} руб. ({recipe.description})")
        print(f"{len(recipes) + 1}. Создать свой рецепт")

        try:
            choice = int(input("Выберите рецепт: ")) - 1
        except ValueError:
            print("Неверный ввод!")
            return

        if choice == len(recipes):
            pizza = self.create_custom_pizza()
        elif 0 <= choice < len(recipes):
            pizza = Pizza(recipes[choice])
        else:
            print("Неверный выбор!")
            return

        print("\nХотите добавить дополнительные начинки?")
        print("1. Да")
        print("2. Нет")

        if input("Ваш выбор: ") == "1":
            self.add_toppings(pizza)

        print("\nВыберите тип цены:")
        print("1. Стандартная цена")
        print("2. Со скидкой 10%")

        price_choice = input("Ваш выбор: ")

        if price_choice == "2":
            strategy = DiscountPriceStrategy(10)
        else:
            strategy = StandardPriceStrategy()

        order = self.order_manager.create_order(pizza, strategy)

        print("\nЗаказ создан!")
        print(f"Номер заказа: #{order.order_id}")
        print(f"Пицца: {pizza.name}")
        print(f"Начинки: {', '.join(t.name for t in pizza.all_toppings) if pizza.all_toppings else 'нет'}")
        print(f"Стоимость: {order.total_price:.2f} руб.")
        print(f"Прибыль: {order.profit:.2f} руб.")

    def create_custom_pizza(self) -> Pizza:
        """Создает пользовательскую пиццу по индивидуальному рецепту"""

        print("\nСоздание своего рецепта")
        name = input("Введите название пиццы: ")

        try:
            base_price = float(input("Введите базовую цену: "))
            base_cost = float(input("Введите себестоимость: "))
        except ValueError:
            print("Неверный формат числа!")
            return self.create_custom_pizza()

        description = input("Введите описание: ")

        print("\nВыберите начинки:")
        for i, topping in enumerate(self.available_toppings, 1):
            print(f"{i}. {topping.name} - {topping.price} руб.")

        choices = input("Введите номера начинок через запятую: ")
        selected_indices = [int(x.strip()) - 1 for x in choices.split(",") if x.strip().isdigit()]

        toppings = [self.available_toppings[i] for i in selected_indices
                    if 0 <= i < len(self.available_toppings)]

        recipe = PizzaFactory.create_custom_recipe(name, base_price, base_cost, toppings, description)
        return Pizza(recipe)

    def add_toppings(self, pizza: Pizza):
        """Добавляет дополнительные начинки к пицце"""

        print("\nДобавление начинко:")
        for i, topping in enumerate(self.available_toppings, 1):
            print(f"{i}. {topping.name} - {topping.price} руб.")

        print("0. Завершить добавление")

        while True:
            try:
                choice = int(input("Выберите начинку (0 для завершения): "))
            except ValueError:
                print("Неверный ввод!")
                continue

            if choice == 0:
                break
            elif 1 <= choice <= len(self.available_toppings):
                pizza.custom_toppings.append(self.available_toppings[choice - 1])
                print(f"Добавлен: {self.available_toppings[choice - 1].name}")
            else:
                print("Неверный выбор!")

    def show_statistics(self):
        """Отображает общую статистику пиццерии"""
        stats = self.order_manager.get_total_statistics()
        print("\nСтатистика пиццерии:")
        print(f"Всего заказов: {stats['total_orders']}")
        print(f"Общая выручка: {stats['total_revenue']:.2f} руб.")
        print(f"Общая себестоимость: {stats['total_cost']:.2f} руб.")
        print(f"Общая прибыль: {stats['total_profit']:.2f} руб.")

    def admin_panel(self):
        """Панель администратора для управления рецептами"""

        print("\nАдмин-панель")
        password = input("Введите пароль (admin): ")

        if password != "admin":
            print("Неверный пароль!")
            return

        while True:
            print("\nМеню админа:")
            print("1. Просмотреть все рецепты")
            print("2. Добавить рецепт")
            print("3. Удалить рецепт")
            print("4. Сохранить рецепты в файл")
            print("5. Загрузить рецепты из файла")
            print("6. Назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.view_all_recipes()
            elif choice == "2":
                self.add_recipe_admin()
            elif choice == "3":
                self.delete_recipe_admin()
            elif choice == "4":
                PizzaFactory.save_recipes()
                print("Рецепты сохранены!")
            elif choice == "5":
                PizzaFactory.load_recipes()
                print("Рецепты загружены!")
            elif choice == "6":
                break
            else:
                print("Неверный выбор!")

    def view_all_recipes(self):
        """Отображает все доступные рецепты пицц"""

        recipes = PizzaFactory.get_all_recipes()
        print("\nВсе рецепты:")
        for recipe in recipes:
            print(f"\n{recipe.name}:")
            print(f"  Цена: {recipe.base_price} руб.")
            print(f"  Себестоимость: {recipe.base_cost} руб.")
            print(f"  Описание: {recipe.description}")
            if recipe.toppings:
                print(f"  Начинки: {', '.join(t.name for t in recipe.toppings)}")

    def add_recipe_admin(self):
        """Добавляет новый рецепт через админ-панель"""

        print("\nДобавление нового рецепта")
        name = input("Название: ")

        try:
            base_price = float(input("Базовая цена: "))
            base_cost = float(input("Себестоимость: "))
        except ValueError:
            print("Неверный формат числа!")
            return

        description = input("Описание: ")

        toppings = []
        print("\nДоступные начинки:")
        for i, topping in enumerate(self.available_toppings, 1):
            print(f"{i}. {topping.name}")

        choice = input("Введите номера начинок через запятую: ")
        selected_indices = [int(x.strip()) - 1 for x in choice.split(",") if x.strip().isdigit()]

        for idx in selected_indices:
            if 0 <= idx < len(self.available_toppings):
                toppings.append(self.available_toppings[idx])

        PizzaFactory.create_custom_recipe(name, base_price, base_cost, toppings, description)
        print(f"Рецепт '{name}' добавлен!")

    def delete_recipe_admin(self):
        """Удаляет рецепт через админ-панель"""

        recipes = PizzaFactory.get_all_recipes()
        print("\nУдаление рецепта")

        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe.name}")

        try:
            choice = int(input("Выберите рецепт для удаления: ")) - 1
        except ValueError:
            print("Неверный ввод!")
            return

        if 0 <= choice < len(recipes):
            name = recipes[choice].name
            PizzaFactory.delete_recipe(name)
            print(f"Рецепт '{name}' удален!")
        else:
            print("Неверный выбор!")


if __name__ == '__main__':
    PizzaFactory.load_recipes()

    ui = UserInterface()
    ui.show_main_menu()

    PizzaFactory.save_recipes()


