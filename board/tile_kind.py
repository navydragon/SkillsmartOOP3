"""Типы фишек для игры Три-в-ряд."""

from enum import Enum


class TileKind(Enum):
    """Типы фишек в игре."""
    
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    
    @classmethod
    def all(cls):
        """Получить все типы фишек.
        
        Returns:
            list[TileKind]: Список всех типов фишек
        """
        return [cls.A, cls.B, cls.C, cls.D, cls.E]
