import pytest

from src.category import Category
from src.exceptions import ZeroQuantityError
from src.lawn_grass import LawnGrass
from src.order import Order
from src.product import Product
from src.smartphone import Smartphone


@pytest.mark.parametrize(
    "factory",
    [
        lambda: Product("Товар", "Описание", 100, 0),
        lambda: Product.new_product(dict(name="Товар", description="Описание", price=100, quantity=0)),
        lambda: Smartphone("Телефон", "Описание", 100, 0, 90, "Модель", 128, "Белый"),
        lambda: LawnGrass("Трава", "Описание", 100, 0, "Россия", "7 дней", "Зеленый"),
    ],
)
def test_zero_stock_creation(factory, capsys):
    with pytest.raises(ValueError, match="^Товар с нулевым количеством не может быть добавлен$"):
        factory()
    assert capsys.readouterr().out == ""
    assert Category.product_count == 0


def test_middle_price_ignores_stock_and_other_categories(product):
    category = Category("Техника", "", [product, Product("Книга", "", 100, 1)])
    Category("Другая", "", [Product("Другой", "", 900, 2)])
    assert category.middle_price() == 12550
    product.price = 30000
    assert category.middle_price() == 15050
    category.add_product(Product("Еще", "", 200, 2))
    assert category.middle_price() == 10100


def test_empty_middle_price():
    assert Category("Пустая", "", []).middle_price() == 0


@pytest.mark.parametrize("target", ["category", "order"])
def test_reject_depleted_product(target, product, capsys):
    category = Category("Категория", "", [product])
    depleted = Product("Закончился", "", 100, 1)
    depleted.quantity = 0
    capsys.readouterr()
    with pytest.raises(ZeroQuantityError, match="Товар с нулевым количеством не может быть добавлен"):
        if target == "category":
            category.add_product(depleted)
        else:
            Order(depleted, 1)
    assert capsys.readouterr().out.splitlines() == [
        "Товар с нулевым количеством не может быть добавлен",
        "Обработка добавления товара завершена",
    ]
    assert len(category) == 1
    assert category[0] is product
    assert Category.product_count == 1
    assert depleted.quantity == 0


@pytest.mark.parametrize("target", ["category", "order"])
def test_success_messages(target, product, capsys):
    category = Category("Категория", "", [])
    capsys.readouterr()
    if target == "category":
        category.add_product(product)
        destination = "категорию"
    else:
        Order(product, 1)
        destination = "заказ"
    assert capsys.readouterr().out.splitlines() == [
        f"Товар добавлен в {destination}",
        "Обработка добавления товара завершена",
    ]


@pytest.mark.parametrize("target", ["category", "order"])
def test_final_message_on_type_error(target, capsys):
    category = Category("Категория", "", [])
    with pytest.raises(TypeError):
        if target == "category":
            category.add_product(None)
        else:
            Order(None, 1)
    assert capsys.readouterr().out == "Обработка добавления товара завершена\n"
    assert Category.product_count == 0
