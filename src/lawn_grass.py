from src.product import Product


class LawnGrass(Product):
    """Газонная трава с данными о производителе и прорастании."""

    _repr_fields = Product._repr_fields + ("country", "germination_period", "color")

    country: str
    germination_period: str
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        self.country = country
        self.germination_period = germination_period
        self.color = color
        # Миксин выводит все поля после их заполнения.
        super().__init__(name, description, price, quantity)
