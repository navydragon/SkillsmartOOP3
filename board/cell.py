"""Координаты ячейки на игровой доске."""

from typing import Tuple


class Cell:
    """Ячейка на игровой доске."""
    
    def __init__(self, row: int, col: int):
        """Создать ячейку.
        
        Args:
            row: Номер строки (0-7)
            col: Номер столбца (0-7)
        """
        self._row = row
        self._col = col
    
    def row(self) -> int:
        """Получить номер строки.
        
        Returns:
            int: Номер строки
        """
        return self._row
    
    def col(self) -> int:
        """Получить номер столбца.
        
        Returns:
            int: Номер столбца
        """
        return self._col
    
    def is_valid(self) -> bool:
        """Проверить, находятся ли координаты в допустимом диапазоне.
        
        Returns:
            bool: True если координаты валидны (0-7)
        """
        return 0 <= self._row < 8 and 0 <= self._col < 8
    
    def is_adjacent(self, other: 'Cell') -> bool:
        """Проверить, является ли ячейка соседней.
        
        Args:
            other: Другая ячейка
            
        Returns:
            bool: True если ячейки соседние по стороне
        """
        if not isinstance(other, Cell):
            return False
        
        row_diff = abs(self._row - other._row)
        col_diff = abs(self._col - other._col)
        
        # Соседние по стороне (не по диагонали)
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
    
    def __eq__(self, other) -> bool:
        """Проверить равенство ячеек.
        
        Args:
            other: Другая ячейка
            
        Returns:
            bool: True если координаты одинаковые
        """
        if not isinstance(other, Cell):
            return False
        return self._row == other._row and self._col == other._col
    
    def __hash__(self) -> int:
        """Получить хеш ячейки.
        
        Returns:
            int: Хеш ячейки
        """
        return hash((self._row, self._col))
    
    def __str__(self) -> str:
        """Строковое представление ячейки.
        
        Returns:
            str: Координаты в формате (row, col)
        """
        return f"({self._row}, {self._col})"
    
    def __repr__(self) -> str:
        """Представление ячейки для отладки.
        
        Returns:
            str: Отладочное представление
        """
        return f"Cell({self._row}, {self._col})"
