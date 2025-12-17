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