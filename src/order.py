from src.base_entity import BaseEntity
from src.product import Product


class Order(BaseEntity):
    """Заказ одного товара с количеством и стоимостью покупки."""

    def __init__(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise TypeError("В заказе должен быть один объект Product или его наследник")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Количество должно быть положительным целым числом")
        self.product = product
        self.quantity = quantity
        self.__total_price = product.price * quantity

    @property
    def total_price(self) -> float:
        """Возвращает стоимость, зафиксированную при создании заказа."""
        return self.__total_price

    def __str__(self) -> str:
        return f"Заказ: {self.product.name}, количество: {self.quantity} шт. Стоимость: {self.total_price} руб."
