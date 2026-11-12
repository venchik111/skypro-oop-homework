import inspect

import pytest

from src.base_entity import BaseEntity
from src.base_product import BaseProduct
from src.category import Category
from src.lawn_grass import LawnGrass
from src.logging_mixin import LoggingMixin
from src.order import Order
from src.product import Product
from src.smartphone import Smartphone


def test_base_product_is_abstract():
    assert inspect.isabstract(BaseProduct)
    with pytest.raises(TypeError):
        BaseProduct()

    class IncompleteProduct(BaseProduct):
        pass

    with pytest.raises(TypeError):
        IncompleteProduct()


def test_product_inheritance(product):
    assert isinstance(product, BaseProduct)
    assert isinstance(product, LoggingMixin)
    assert not inspect.isabstract(Product)
    assert Smartphone.__bases__ == (Product,)
    assert LawnGrass.__bases__ == (Product,)


def test_product_creation_log(capsys):
    product = Product("Продукт1", "Описание продукта", 1200, 10)
    expected = "Product('Продукт1', 'Описание продукта', 1200, 10)"
    assert capsys.readouterr().out == expected + "\n"
    assert repr(product) == expected


def test_smartphone_creation_log(capsys):
    phone = Smartphone("Телефон", "256 ГБ", 100, 10, 95.5, "S23", 256, "Серый")
    expected = "Smartphone('Телефон', '256 ГБ', 100, 10, 95.5, 'S23', 256, 'Серый')"
    assert capsys.readouterr().out == expected + "\n"
    assert repr(phone) == expected


def test_lawn_grass_creation_log(capsys):
    grass = LawnGrass("Трава", "Для газона", 200, 2, "Россия", "7 дней", "Зеленый")
    expected = "LawnGrass('Трава', 'Для газона', 200, 2, 'Россия', '7 дней', 'Зеленый')"
    assert capsys.readouterr().out == expected + "\n"
    assert repr(grass) == expected


def test_classmethod_logs_creation(capsys):
    product = Product.new_product({"name": "Книга", "description": "Python", "price": 80, "quantity": 15})
    assert capsys.readouterr().out == "Product('Книга', 'Python', 80, 15)\n"
    assert product.quantity == 15


def test_repr_escapes_quotes_and_newlines(capsys):
    product = Product("Книга 'Python'", "Строка\nЕще строка", 80, 15)
    output = capsys.readouterr().out
    assert output == repr(product) + "\n"
    restored = eval(repr(product), {"Product": Product})
    assert restored.name == product.name
    assert restored.description == product.description


def test_repr_uses_current_values(product):
    product.price = 30000
    product.quantity = 2
    assert repr(product) == "Product('Телефон', '128 ГБ', 30000, 2)"


def test_base_entity_is_abstract():
    assert inspect.isabstract(BaseEntity)
    with pytest.raises(TypeError):
        BaseEntity()

    class IncompleteEntity(BaseEntity):
        pass

    with pytest.raises(TypeError):
        IncompleteEntity()


def test_order_init(product):
    order = Order(product, 2)
    assert isinstance(order, BaseEntity)
    assert order.product is product
    assert order.quantity == 2
    assert order.total_price == 50000.0
    assert product.quantity == 10
    assert str(order) == "Заказ: Телефон, количество: 2 шт. Стоимость: 50000.0 руб."


def test_order_price_is_fixed(product):
    order = Order(product, 2)
    product.price = 30000
    assert order.total_price == 50000.0


@pytest.mark.parametrize("invalid", ["Товар", [], None, Product])
def test_order_rejects_non_product(invalid):
    with pytest.raises(TypeError):
        Order(invalid, 1)


@pytest.mark.parametrize("quantity", [0, -1, 1.5, "2", True])
def test_order_rejects_invalid_quantity(product, quantity):
    with pytest.raises(ValueError):
        Order(product, quantity)


def test_order_accepts_product_subclass():
    phone = Smartphone("Телефон", "256 ГБ", 100, 10, 95.5, "S23", 256, "Серый")
    assert Order(phone, 2).total_price == 200


def test_category_total_price(category, product):
    assert isinstance(category, BaseEntity)
    assert category.total_price == 250000.0
    category.add_product(Product("Книга", "Учебник", 80, 15))
    assert category.total_price == 251200.0
    product.price = 30000
    assert category.total_price == 301200.0
    assert Category.product_count == 2


def test_empty_category_total_price():
    category = Category("Пустая", "Нет товаров", [])
    assert category.total_price == 0
