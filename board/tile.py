"""Представление фишки на игровой доске."""

from .tile_kind import TileKind


class Tile:
    """Фишка на игровой доске."""
    
    def __init__(self, kind: TileKind):
        """Создать фишку.
        
        Args:
            kind: Тип фишки
        """
        self._kind = kind
    
    def kind(self) -> TileKind:
        """Получить тип фишки.
        
        Returns:
            TileKind: Тип фишки
        """
        return self._kind
    
    def __eq__(self, other) -> bool:
        """Проверить равенство фишек.
        
        Args:
            other: Другая фишка
            
        Returns:
            bool: True если типы фишек одинаковые
        """
        if not isinstance(other, Tile):
            return False
        return self._kind == other._kind
    
    def __hash__(self) -> int:
        """Получить хеш фишки.
        
        Returns:
            int: Хеш фишки
        """
        return hash(self._kind)
    
    def __str__(self) -> str:
        """Строковое представление фишки.
        
        Returns:
            str: Символ типа фишки
        """
        return self._kind.value
    
    def __repr__(self) -> str:
        """Представление фишки для отладки.
        
        Returns:
            str: Отладочное представление
        """
        return f"Tile({self._kind.value})"
