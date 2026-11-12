from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Общий интерфейс товара: создание, цена, вывод и сложение."""

    name: str
    description: str
    quantity: int

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: dict, products: list | None = None):
        """Создает товар из словаря."""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Возвращает цену товара."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает описание товара."""
        pass

    @abstractmethod
    def __add__(self, other):
        """Возвращает стоимость остатков двух товаров."""
        pass
