import json

from src.category import Category
from src.product import Product


def load_categories(file_path) -> list[Category]:
    """Читает JSON и создает категории с объектами товаров."""
    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        products = []
        for product_data in category_data["products"]:
            product = Product(
                product_data["name"],
                product_data["description"],
                product_data["price"],
                product_data["quantity"],
            )
            products.append(product)
        category = Category(category_data["name"], category_data["description"], products)
        categories.append(category)
    return categories
