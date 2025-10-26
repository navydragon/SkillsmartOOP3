"""Стандартная реализация генератора случайных значений."""

import random as random_module
from typing import Optional

from .random_provider import RandomProvider
from board.tile_kind import TileKind


class RandomProviderDefault(RandomProvider):
    """Стандартная реализация поставщика случайностей."""
    
    def __init__(self, seed: Optional[int] = None):
        """Инициализировать генератор.
        
        Args:
            seed: Начальное значение (None для системного)
        """
        self._random = random_module.Random(seed)
        self._tile_kinds = list(TileKind.all())
    
    def next_tile_kind(self) -> TileKind:
        """Получить следующий случайный тип фишки.
        
        Returns:
            TileKind: Случайный тип фишки
        """
        return self._random.choice(self._tile_kinds)
    
    def set_seed(self, seed: int) -> None:
        """Установить seed генератора.
        
        Args:
            seed: Новое начальное значение
        """
        self._random.seed(seed)
