class Product:
    """Товар интернет-магазина."""

    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, products: list | None = None):
        """Создает товар из словаря, объединяя его с одноименным товаром."""
        product = cls(
            product_data["name"], product_data["description"], product_data["price"], product_data["quantity"]
        )
        if products is not None:
            for existing in products:
                if existing.name == product.name:
                    product.quantity += existing.quantity
                    product.__price = max(product.price, existing.price)
        return product

    @property
    def price(self) -> float:
        """Возвращает цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Меняет цену, запрашивая подтверждение при снижении."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self.__price:
            answer = input("Подтвердите снижение цены (y/n): ")
            if answer != "y":
                return
        self.__price = new_price

    def __str__(self) -> str:
        """Возвращает название, цену и остаток товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Возвращает полную стоимость остатков двух товаров."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity
