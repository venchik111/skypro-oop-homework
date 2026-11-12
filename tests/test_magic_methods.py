import pytest

from src.category import Category
from src.product import Product
from src.product_iterator import ProductIterator


def test_product_str(product):
    assert str(product) == "Телефон, 25000.0 руб. Остаток: 10 шт."


def test_product_str_integer_price():
    product = Product("Книга", "Учебник", 80, 15)
    assert str(product) == "Книга, 80 руб. Остаток: 15 шт."


def test_product_str_updates(product):
    product.price = 30000
    product.quantity = 0
    assert str(product) == "Телефон, 30000 руб. Остаток: 0 шт."


def test_category_str(category):
    assert str(category) == "Смартфоны, количество продуктов: 10 шт."


def test_category_str_sums_stock(category):
    category.add_product(Product("Ноутбук", "16 ГБ", 70000.0, 20))
    Category("Другая категория", "Не входит в сумму", [Product("Книга", "Учебник", 80, 100)])
    assert str(category) == "Смартфоны, количество продуктов: 30 шт."
    assert Category.product_count == 3


def test_category_str_updates(category, product):
    product.quantity = 4
    assert str(category) == "Смартфоны, количество продуктов: 4 шт."


def test_empty_category_str():
    category = Category("Пустая", "Нет товаров", [])
    assert str(category) == "Пустая, количество продуктов: 0 шт."
    assert category.products == ""


def test_products_getter_uses_str(category, monkeypatch):
    monkeypatch.setattr(Product, "__str__", lambda self: "Описание товара")
    assert category.products == "Описание товара\n"


def test_add_products():
    first = Product("Первый", "Описание", 100, 10)
    second = Product("Второй", "Описание", 200, 2)
    assert first + second == 1400
    assert second + first == 1400
    assert first.price == 100
    assert first.quantity == 10
    assert second.price == 200
    assert second.quantity == 2


def test_add_products_fractional_price():
    first = Product("Первый", "Описание", 99.9, 3)
    second = Product("Второй", "Описание", 150.5, 2)
    assert first + second == pytest.approx(600.7)


def test_add_products_without_stock(product):
    empty = Product("Пустой", "Нет на складе", 100, 0)
    assert product + empty == 250000.0
    assert empty + empty == 0
    assert product + product == 500000.0


def test_add_unsupported_type(product):
    with pytest.raises(TypeError):
        product + 100


def test_category_len_and_index(category, product):
    assert len(category) == 1
    assert category[0] is product
    with pytest.raises(IndexError):
        category[1]


def test_product_iterator(category, product):
    other = Product("Ноутбук", "16 ГБ", 70000.0, 2)
    category.add_product(other)
    iterator = ProductIterator(category)
    assert iter(iterator) is iterator
    assert next(iterator) is product
    assert next(iterator) is other
    with pytest.raises(StopIteration):
        next(iterator)
    with pytest.raises(StopIteration):
        next(iterator)


def test_iterator_for_loop(category, product):
    products = []
    for item in ProductIterator(category):
        products.append(item)
    assert products == [product]


def test_empty_iterator():
    iterator = ProductIterator(Category("Пустая", "Без товаров", []))
    assert list(iterator) == []
    with pytest.raises(StopIteration):
        next(iterator)


def test_repeat_iteration(category, product):
    iterator = ProductIterator(category)
    assert list(iterator) == [product]
    assert list(iterator) == [product]


def test_iterators_are_independent(category, product):
    first = ProductIterator(category)
    second = ProductIterator(category)
    assert next(first) is product
    assert next(second) is product
    with pytest.raises(StopIteration):
        next(first)
