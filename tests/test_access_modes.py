import pytest

from src.category import Category
from src.product import Product


def test_add_product(category):
    product = Product("Ноутбук", "16 ГБ", 70000.0, 20)
    result = category.add_product(product)
    assert result is None
    assert category.products == ("Телефон, 25000.0 руб. Остаток: 10 шт.\n" "Ноутбук, 70000.0 руб. Остаток: 20 шт.\n")
    assert Category.product_count == 2
    assert Category.category_count == 1


def test_add_product_to_empty_category(product):
    category = Category("Техника", "Для дома", [])
    category.add_product(product)
    assert category.products == "Телефон, 25000.0 руб. Остаток: 10 шт.\n"
    assert Category.product_count == 1


def test_products_are_private(category):
    with pytest.raises(AttributeError):
        category.__products
    with pytest.raises(AttributeError):
        category.products = []


def test_constructor_does_not_keep_external_list(product):
    products = [product]
    category = Category("Техника", "Для дома", products)
    products.clear()
    assert category.products == "Телефон, 25000.0 руб. Остаток: 10 шт.\n"
    assert Category.product_count == 1


def test_products_format_with_integer_price():
    category = Category("Книги", "Учебники", [Product("Python", "Учебник", 80, 15)])
    assert category.products == "Python, 80 руб. Остаток: 15 шт.\n"


def test_products_show_updated_data(category, product):
    product.price = 30000.0
    product.quantity = 0
    assert category.products == "Телефон, 30000.0 руб. Остаток: 0 шт.\n"


def test_new_product():
    data = {"name": "Телефон", "description": "128 ГБ", "price": 25000.0, "quantity": 10}
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "Телефон"
    assert product.description == "128 ГБ"
    assert product.price == 25000.0
    assert product.quantity == 10
    assert data["quantity"] == 10
    assert Category.product_count == 0


@pytest.mark.parametrize("price, expected", [(20000, 25000.0), (30000, 30000), (25000, 25000)])
def test_new_product_merges_duplicates(product, price, expected):
    data = {"name": "Телефон", "description": "Новая поставка", "price": price, "quantity": 3}
    other = Product("Ноутбук", "16 ГБ", 70000.0, 20)
    products = [other, product]
    result = Product.new_product(data, products)
    assert result.name == "Телефон"
    assert result.description == "Новая поставка"
    assert result.quantity == 13
    assert result.price == expected
    assert result is not product
    assert product.quantity == 10
    assert data["quantity"] == 3
    assert products == [other, product]


@pytest.mark.parametrize("products", [[], [Product("Книга", "Учебник", 500.0, 2)]])
def test_new_product_without_duplicates(products):
    data = {"name": "Телефон", "description": "128 ГБ", "price": 25000.0, "quantity": 10}
    result = Product.new_product(data, products)
    assert result.name == "Телефон"
    assert result.price == 25000.0
    assert result.quantity == 10


def test_price_is_private(product):
    with pytest.raises(AttributeError):
        product.__price
    assert product.price == 25000.0


@pytest.mark.parametrize("price", [0, -100])
def test_invalid_price(product, price, capsys, monkeypatch):
    def unexpected_input(prompt):
        pytest.fail("Для некорректной цены подтверждение не требуется")

    monkeypatch.setattr("builtins.input", unexpected_input)
    product.price = price
    assert product.price == 25000.0
    assert capsys.readouterr().out == "Цена не должна быть нулевая или отрицательная\n"


@pytest.mark.parametrize("price", [25000.0, 30000.0])
def test_price_without_confirmation(product, price, monkeypatch):
    def unexpected_input(prompt):
        pytest.fail("При сохранении или повышении цены подтверждение не требуется")

    monkeypatch.setattr("builtins.input", unexpected_input)
    product.price = price
    assert product.price == price


@pytest.mark.parametrize("answer, expected", [("y", 20000), ("n", 25000.0), ("", 25000.0), ("yes", 25000.0)])
def test_price_reduction_confirmation(product, monkeypatch, answer, expected):
    monkeypatch.setattr("builtins.input", lambda prompt: answer)
    product.price = 20000
    assert product.price == expected
