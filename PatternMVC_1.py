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

