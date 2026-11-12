from src.product import Product


class Smartphone(Product):
    """Смартфон с характеристиками производительности, памяти и модели."""

    _repr_fields = Product._repr_fields + ("efficiency", "model", "memory", "color")

    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        # Миксин выводит все поля после их заполнения.
        super().__init__(name, description, price, quantity)
