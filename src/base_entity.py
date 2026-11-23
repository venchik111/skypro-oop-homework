from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """Общий интерфейс категории и заказа."""

    @property
    @abstractmethod
    def total_price(self) -> float:
        """Возвращает общую стоимость товаров."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает описание сущности."""
        pass
