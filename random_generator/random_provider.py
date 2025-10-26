"""Абстрактный интерфейс для генерации случайных значений."""

from abc import ABC, abstractmethod
from board.tile_kind import TileKind


class RandomProvider(ABC):
    """Абстрактный интерфейс для генерации случайных значений."""
    
    @abstractmethod
    def next_tile_kind(self) -> TileKind:
        """Получить следующий случайный тип фишки.
        
        Returns:
            TileKind: Случайный тип фишки
        """
        pass
