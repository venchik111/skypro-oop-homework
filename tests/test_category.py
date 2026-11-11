from src.category import Category
from src.product import Product


def test_category_init(category, product):
    assert category.name == "Смартфоны"
    assert category.description == "Мобильные телефоны"
    assert category.products == [product]
    assert isinstance(category.products, list)
    assert isinstance(category.products[0], Product)


def test_category_count(category):
    other = Category("Пустая категория", "Без товаров", [])
    assert Category.category_count == 2
    assert category.category_count == 2
    assert other.category_count == 2
    assert other.products == []
    assert Category.product_count == 1


def test_product_count(category, product):
    other_product = Product("Ноутбук", "16 ГБ", 70000.0, 20)
    other = Category("Техника", "Для дома", [product, other_product])
    assert Category.product_count == 3
    assert category.product_count == 3
    assert other.product_count == 3


def test_empty_category():
    Category("Пустая", "Нет товаров", [])
    assert Category.category_count == 1
    assert Category.product_count == 0
