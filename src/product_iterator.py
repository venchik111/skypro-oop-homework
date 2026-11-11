from src.category import Category
from src.product import Product


class ProductIterator:
    """Перебирает товары одной категории в порядке добавления."""

    def __init__(self, category: Category):
        self.category = category
        self.index = 0

    def __iter__(self):
        """Начинает перебор с первого товара, как в примере урока."""
        self.index = 0
        return self

    def __next__(self) -> Product:
        """Возвращает следующий товар или завершает перебор."""
        if self.index < len(self.category):
            product = self.category[self.index]
            self.index += 1
            return product
        raise StopIteration
