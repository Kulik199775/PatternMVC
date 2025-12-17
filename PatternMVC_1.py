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