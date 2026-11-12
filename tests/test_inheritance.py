import pytest

from src.category import Category
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


@pytest.fixture
def smartphone():
    return Smartphone("Телефон", "256 ГБ", 100.0, 10, 95.5, "S23", 256, "Серый")


@pytest.fixture
def lawn_grass():
    return LawnGrass("Трава", "Для газона", 200.0, 2, "Россия", "7 дней", "Зеленый")


def test_smartphone_init(smartphone):
    assert isinstance(smartphone, Product)
    assert issubclass(Smartphone, Product)
    assert smartphone.name == "Телефон"
    assert smartphone.description == "256 ГБ"
    assert smartphone.price == 100.0
    assert smartphone.quantity == 10
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_lawn_grass_init(lawn_grass):
    assert isinstance(lawn_grass, Product)
    assert issubclass(LawnGrass, Product)
    assert lawn_grass.name == "Трава"
    assert lawn_grass.description == "Для газона"
    assert lawn_grass.price == 200.0
    assert lawn_grass.quantity == 2
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7 дней"
    assert lawn_grass.color == "Зеленый"


def test_same_class_addition(smartphone, lawn_grass):
    phone = Smartphone("Другой телефон", "512 ГБ", 200.0, 2, 98.2, "15", 512, "Белый")
    grass = LawnGrass("Другая трава", "Для дачи", 100.0, 10, "США", "5 дней", "Зеленый")
    assert smartphone + phone == 1400.0
    assert phone + smartphone == 1400.0
    assert lawn_grass + grass == 1400.0
    assert grass + lawn_grass == 1400.0


def test_different_classes_cannot_be_added(smartphone, lawn_grass, product):
    for first, second in [(smartphone, lawn_grass), (smartphone, product), (lawn_grass, product)]:
        with pytest.raises(TypeError):
            first + second
        with pytest.raises(TypeError):
            second + first


def test_inherited_properties(smartphone, lawn_grass, monkeypatch):
    assert str(smartphone) == "Телефон, 100.0 руб. Остаток: 10 шт."
    assert str(lawn_grass) == "Трава, 200.0 руб. Остаток: 2 шт."
    smartphone.price = 150.0
    assert smartphone.price == 150.0
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    lawn_grass.price = 100.0
    assert lawn_grass.price == 100.0


def test_category_accepts_products_and_subclasses(smartphone, lawn_grass, product):
    category = Category("Товары", "Все товары", [product, smartphone])
    assert category.add_product(lawn_grass) is None
    assert len(category) == 3
    assert category[0] is product
    assert category[1] is smartphone
    assert category[2] is lawn_grass
    assert Category.category_count == 1
    assert Category.product_count == 3


@pytest.mark.parametrize("invalid", ["Товар", 42, 3.14, None, [], {}, Product, Smartphone, object()])
def test_category_rejects_other_objects(category, invalid):
    before = category.products
    with pytest.raises(TypeError):
        category.add_product(invalid)
    assert category.products == before
    assert len(category) == 1
    assert Category.product_count == 1
    assert Category.category_count == 1


def test_category_constructor_rejects_other_objects():
    with pytest.raises(TypeError):
        Category("Ошибка", "Некорректный товар", ["Не продукт"])
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_other_product_subclass_is_accepted():
    class Book(Product):
        pass

    book = Book("Python", "Учебник", 80, 15)
    category = Category("Книги", "Учебники", [])
    category.add_product(book)
    assert category[0] is book
    assert Category.product_count == 1
    with pytest.raises(TypeError):
        book + Product("Книга", "Описание", 80, 1)


def test_inherited_new_product():
    data = {
        "name": "Телефон",
        "description": "256 ГБ",
        "price": 100.0,
        "quantity": 10,
        "efficiency": 95.5,
        "model": "S23",
        "memory": 256,
        "color": "Серый",
    }
    phone = Smartphone.new_product(data)
    assert isinstance(phone, Smartphone)
    assert phone.model == "S23"
    assert phone.memory == 256
    grass = LawnGrass.new_product(
        {
            "name": "Трава",
            "description": "Для газона",
            "price": 200.0,
            "quantity": 2,
            "country": "Россия",
            "germination_period": "7 дней",
            "color": "Зеленый",
        }
    )
    assert isinstance(grass, LawnGrass)
    assert grass.country == "Россия"
