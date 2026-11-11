from src.product import Product


class Category:
    """Категория со списком товаров и общими счетчиками."""

    name: str
    description: str
    products: list[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        # Считаем позиции в списке, а не остатки товаров на складе.
        Category.product_count += len(products)
