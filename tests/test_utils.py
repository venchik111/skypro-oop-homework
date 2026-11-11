import json
from pathlib import Path

import pytest

from src.category import Category
from src.utils import load_categories


def test_load_categories():
    path = Path(__file__).parent.parent / "data" / "products.json"
    categories = load_categories(path)
    assert len(categories) == 2
    assert isinstance(categories[0], Category)
    assert categories[0].name == "Смартфоны"
    assert categories[0].products == (
        "Samsung Galaxy C23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"
    )
    assert categories[1].name == "Телевизоры"
    assert Category.category_count == 2
    assert Category.product_count == 4


def test_empty_file_data(tmp_path):
    path = tmp_path / "empty.json"
    path.write_text("[]", encoding="utf-8")
    assert load_categories(path) == []
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_category_without_products(tmp_path):
    path = tmp_path / "category.json"
    data = [{"name": "Книги", "description": "Учебники", "products": []}]
    path.write_text(json.dumps(data), encoding="utf-8")
    categories = load_categories(path)
    assert categories[0].description == "Учебники"
    assert categories[0].products == ""
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_categories(tmp_path / "missing.json")


def test_invalid_json(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_categories(path)
