# Модель
class Shoe:
    def __init__(self, shoe_id, shoe_type, shoe_kind, color, price, manufacturer, size):
        self.shoe_id = shoe_id
        self.shoe_type = shoe_type
        self.shoe_kind = shoe_kind
        self.color = color
        self.price = price
        self.manufacturer = manufacturer
        self.size = size

    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'id': self.shoe_id,
            'type': self.shoe_type,
            'kind': self.shoe_kind,
            'color': self.color,
            'price': self.price,
            'manufacturer': self.manufacturer,
            'size': self.size
        }

    def __str__(self):
        return f'{self.shoe_type} {self.shoe_kind} ({self.color}),размер {self.size}, цена {self.price} руб.'

class ShoeModel:
    def __init__(self):
        self.shoes = []
        self.next_id = 1

    def add_shoe(self, shoe_type, shoe_kind, color, price, manufacturer, size):
        """Добавить новую обувь"""
        shoe = Shoe(self.next_id, shoe_type, shoe_kind, color, price, manufacturer, size)
        self.shoes.append(shoe)
        self.next_id += 1
        return shoe

    def get_all_shoes(self):
        """Получение всей обуви"""
        return self.shoes

    def get_shoe_by_id(self, shoe_id):
        """Найти обувь по id"""
        for shoe in self.shoes:
            if shoe.shoe_id == shoe_id:
                return shoe
        return None

    def update_shoe(self, shoe_id, **kwargs):
        """Обновление данных обуви"""
        shoe = self.get_shoe_by_id(shoe_id)
        if not shoe:
            return False

        for key, value in kwargs.items():
            if hasattr(shoe, key):
                setattr(shoe, key, value)
        return True

    def delete_shoe(self, shoe_id):
        """Удаление обуви"""
        shoe = self.get_shoe_by_id(shoe_id)
        if shoe:
            self.shoes.remove(shoe)
            return True
        return False

    def get_shoes_by_type(self, shoe_type):
        """Получить обувь по типу (муж/жен)"""
        return [shoe for shoe in self.shoes if shoe.shoe_type == shoe_type]

    def get_shoes_by_kind(self, shoe_kind):
        """Получить обувь по виду (кроссовки, сапоги и т.д)"""
        return [shoe for shoe in self.shoes if shoe.shoe_kind == shoe_kind]

    def get_shoes_by_price_range(self, min_price, max_price):
        """Получение обуви в диапазоне цен"""
        return [shoe for shoe in self.shoes if min_price <= shoe.price <= max_price]


# Контроллер
class ShoeController:
    def __init__(self):
        self.model = ShoeModel()

    def create_shoe(self, shoe_type, shoe_kind, color, price, manufacturer, size):
        """Создать новую обувь"""
        if price <= 0:
            return None, 'Цена должна быть положительной'
        if size <= 0:
            return None, 'Размер должен быть положительным'

        shoe = self.model.add_shoe(shoe_type, shoe_kind, color, price, manufacturer, size)
        return shoe, 'Обувь успешно добавлена'

    def get_all_shoes(self):
        """Получение всей обуви"""
        return self.model.get_all_shoes()

    def get_shoe(self, shoe_id):
        """Получить обувь по ID"""
        return self.model.get_shoe_by_id(shoe_id)

    def update_shoe(self, shoe_id, **kwargs):
        """Обновление данных обуви"""
        if self.model.update_shoe(shoe_id, **kwargs)
            return 'Данные обновлены!'
        return 'Обувь не найдена'

    def delete_shoe(self, shoe_id):
        """Удалить обувь"""
        if self.model.delete_shoe(shoe_id):
            return 'Обувь удалена!'
        return 'Обувь не найдена'

    def search_shoes(self, shoe_type, shoe_kind, min_price, max_price):
        """Поиск обуви"""
        return self.model.search_shoes(shoe_type, shoe_kind, min_price, max_price)

# Представление (View)

class ShoeView:
    """Представление"""
    def __init__(self):
        self.controller = ShoeController()

    def show_menu(self):
        """Показ меню для пользователя"""
        print('\n' + '=' * 40)
        print('Магазин обуви')
        print('=' * 40)
        print('1. Добавить обувь')
        print('2. Показать всю обувь')
        print('3. Найти обувь по id')
        print('4. Обновить данные')
        print('5. Удалить обувь')
        print('6. Поиск по категориям')
        print('7. Выход')
        print('=' * 40)

    def add_shoe(self):
        """Добавить новую обувь"""
        print('\n ---Добавить обувь---')

        shoe_type = input('Тип (мужская/женская): ')
        shoe_kind = input('Вид (кроссовки, сапоги и т.п.): ')
        color = input('Цвет: ')

        try:
            price = float(input('Цена: '))
            size = float(input('Размер: '))
        except:
            print('Ошибка: цена и размер должны быть положительными!')
            return

        manufacturer = input('Производитель: ')

        shoe, message = self.controller.add_shoe(shoe_type, shoe_kind, color, price, manufacturer, size)
        print(message)

    def show_all_shoes(self):
        """Показать всю обувь"""
        shoes = self.controller.get_all_shoes()

        if not shoes:
            print('\nОбуви нет в магазине')
            return

        print('\n---Вся обувь---')
        for shoe in shoes:
            print(shoe)
        print(f'Всего: {len(shoes)} пар')

    def find_shoe(self):
        """Найти обувь по id"""
        try:
            shoe_id = int(input('\nВведите id обуви: '))
        except:
            print('Ошибка: id должен быть числом')
            return

        shoe = self.controller.get_shoe(shoe_id)

        if shoe:
            print(f'\nНайдена: {shoe}')
        else:
            print('Обувь не найдена')

    def update_shoe(self):
        """Обновить данные обуви"""
        try:
            shoe_id = int(input('\nВведите id обуви для обновления: '))
        except:
            print('Ошибка! ID должен быть числом.')
            return

        print('Введите новые данные (если не менять, оставьте пустым): ')
        updates = {}

        shoe_type = input('Новый тип: ')
        if shoe_type:
            updates['shoe_type'] = shoe_type

        shoe_kind = input('Новый вид: ')
        if shoe_kind:
            updates['shoe_kind'] = shoe_kind

        color = input('Новый цвет: ')
        if color:
            updates['color'] = color

        price = input('Новая цена: ')
        if price:
            try:
                updates['price'] = float(price)
            except:
                print(f'Ошибка: цена должна быть числом.')
                return

        manufacturer = input('Новый производитель: ')
        if manufacturer:
            updates['manufacturer'] = manufacturer

        size = input('Новый размер: ')
        if size:
            try:
                updates['size'] = float(size)
            except:
                print('Ошибка: размер должен быть числом')
                return

        message = self.controller.update_shoe(shoe_id, **updates)
        print(message)

    def delete_shoe(self):
        """Удалить обувь"""
        try:
            shoe_id = int(input('\nВведите id обуви для удаления: '))
        except:
            print(f'Ошибка: id должен быть числом')
            return

        message = self.controller.delete_shoe(shoe_id)
        print(message)

    def search_shoes(self):
        """Поиск обуви"""
        print('\n---Поиск обуви---')
        print('Оставьте пустым, если не важно')

        shoe_type = input('Тип (муж/жен): ')
        if not shoe_type:
            shoe_type = None

        shoe_kind = input("Вид: ")
        if not shoe_kind:
            shoe_kind = None

        min_price = input("Минимальная цена: ")
        if min_price:
            try:
                min_price = float(min_price)
            except:
                print("Ошибка: цена должна быть числом")
                return
        else:
            min_price = None

        max_price = input("Максимальная цена: ")
        if max_price:
            try:
                max_price = float(max_price)
            except:
                print("Ошибка: цена должна быть числом")
                return
        else:
            max_price = None

        shoes = self.controller.search_shoes(shoe_type, shoe_kind, min_price, max_price)

        if shoes:
            print(f"\nНайдено {len(shoes)} пар:")
            for shoe in shoes:
                print(shoe)
        else:
            print("Ничего не найдено")

    def run(self):
        """Запуск программы"""
        # Добавим тестовые данные
        self.controller.add_shoe("мужская", "кроссовки", "черный", 5000, "Nike", 42)
        self.controller.add_shoe("женская", "туфли", "красный", 3000, "Geox", 37)
        self.controller.add_shoe("мужская", "сапоги", "коричневый", 8000, "Timberland", 43)

        # Главный цикл
        while True:
            self.show_menu()

            choice = input("\nВыберите действие (1-7): ")

            if choice == "1":
                self.add_shoe()
            elif choice == "2":
                self.show_all_shoes()
            elif choice == "3":
                self.find_shoe()
            elif choice == "4":
                self.update_shoe()
            elif choice == "5":
                self.delete_shoe()
            elif choice == "6":
                self.search_shoes()
            elif choice == "7":
                print("\nВыход из программы...")
                break
            else:
                print("Неверный выбор! Введите число от 1 до 7")

            input("\nНажмите Enter чтобы продолжить...")

if __name__ == "__main__":
    app = ShoeView()
    app.run()

