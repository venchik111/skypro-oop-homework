import pytest

from src.category import Category
from src.product import Product


@pytest.fixture(autouse=True)
def reset_counts():
    """Каждый тест начинает подсчет с нуля."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product():
    return Product("Телефон", "128 ГБ", 25000.0, 10)


@pytest.fixture
def category(product):
    return Category("Смартфоны", "Мобильные телефоны", [product])
