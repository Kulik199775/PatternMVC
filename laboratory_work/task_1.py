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