from pathlib import Path

from src.category import Category
from src.utils import load_categories

if __name__ == "__main__":
    data_file = Path(__file__).parent / "data" / "products.json"
    categories = load_categories(data_file)
    for category in categories:
        print(category.name)
        for product in category.products:
            print(f"  {product.name}: {product.price} руб., {product.quantity} шт.")
    print(f"Категорий: {Category.category_count}")
    print(f"Товаров: {Category.product_count}")
