class LoggingMixin:
    """Выводит класс и параметры при создании объекта."""

    def __init__(self):
        super().__init__()
        print(repr(self))

    def __repr__(self) -> str:
        """Формирует запись с параметрами конструктора."""
        values = []
        for field in self._repr_fields:
            values.append(repr(getattr(self, field)))
        return f"{self.__class__.__name__}({', '.join(values)})"
