from pathlib import Path

from src.product_iterator import ProductIterator
from src.utils import load_categories

if __name__ == "__main__":
    data_file = Path(__file__).parent / "data" / "products.json"
    categories = load_categories(data_file)
    for category in categories:
        print(category)
        for product in ProductIterator(category):
            print(product)
