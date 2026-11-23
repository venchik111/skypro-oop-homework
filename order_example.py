from src.category import Category
from src.order import Order
from src.product import Product

if __name__ == "__main__":
    product = Product("Учебник Python", "Основы ООП", 1200, 10)
    category = Category("Книги", "Учебники", [product])
    order = Order(product, 2)
    print(category)
    print(f"Стоимость остатков: {category.total_price} руб.")
    print(order)
