from src.product import Product


class Category:
    """Категория с приватным списком товаров и общими счетчиками."""

    name: str
    description: str
    __products: list[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.__products = []
        for product in products:
            self.add_product(product)
        Category.category_count += 1

    def add_product(self, product: Product):
        """Добавляет товар и увеличивает общий счетчик позиций."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает описание всех товаров, по одному на строку."""
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result

    def __str__(self) -> str:
        """Возвращает название категории и суммарный остаток товаров."""
        quantity = 0
        for product in self.__products:
            quantity += product.quantity
        return f"{self.name}, количество продуктов: {quantity} шт."

    def __len__(self) -> int:
        """Возвращает число товарных позиций для перебора."""
        return len(self.__products)

    def __getitem__(self, index):
        """Возвращает товар по индексу, не открывая сам список."""
        return self.__products[index]
