from src.category import Category
from src.product import Product


def test_product_init(product):
    assert product.name == "Телефон"
    assert product.description == "128 ГБ"
    assert product.price == 25000.0
    assert product.quantity == 10


def test_products_are_independent(product):
    other = Product("Телевизор", "4K", 50000.0, 0)
    assert other.name == "Телевизор"
    assert other.quantity == 0
    assert product.name == "Телефон"
    assert product.quantity == 10
    assert Category.product_count == 0
