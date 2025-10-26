"""Изменяемая реализация игровой доски."""

from typing import List, Optional, Iterable

from .board import Board
from .tile import Tile
from .cell import Cell


class MutableBoard(Board):
    """Изменяемая игровая доска 8x8."""
    
    def __init__(self):
        """Создать пустую доску 8x8."""
        self._tiles: List[List[Optional[Tile]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
    
    def width(self) -> int:
        """Получить ширину доски.
        
        Returns:
            int: Ширина доски (всегда 8)
        """
        return 8
    
    def height(self) -> int:
        """Получить высоту доски.
        
        Returns:
            int: Высота доски (всегда 8)
        """
        return 8
    
    def tile_at(self, cell: Cell) -> Optional[Tile]:
        """Получить фишку в указанной ячейке.
        
        Args:
            cell: Ячейка для проверки
            
        Returns:
            Optional[Tile]: Фишка в ячейке или None
        """
        if not self.is_inside(cell):
            return None
        return self._tiles[cell.row()][cell.col()]
    
    def enumerate_cells(self) -> Iterable[Cell]:
        """Перечислить все ячейки доски.
        
        Returns:
            Iterable[Cell]: Все ячейки доски
        """
        for row in range(8):
            for col in range(8):
                yield Cell(row, col)
    
    def clone(self) -> 'MutableBoard':
        """Создать копию доски.
        
        Returns:
            MutableBoard: Независимая копия доски
        """
        clone = MutableBoard()
        for cell in self.enumerate_cells():
            tile = self.tile_at(cell)
            if tile is not None:
                clone.set_tile(cell, Tile(tile.kind()))
        return clone
    
    def set_tile(self, cell: Cell, tile: Optional[Tile]) -> None:
        """Установить фишку в ячейку.
        
        Args:
            cell: Ячейка для установки
            tile: Фишка для установки (None для очистки)
            
        Raises:
            ValueError: Если ячейка вне доски
        """
        if not self.is_inside(cell):
            raise ValueError(f"Ячейка {cell} вне доски")
        
        self._tiles[cell.row()][cell.col()] = tile
    
    def swap(self, a: Cell, b: Cell) -> None:
        """Обменять содержимое двух ячеек.
        
        Args:
            a: Первая ячейка
            b: Вторая ячейка
            
        Raises:
            ValueError: Если ячейки не соседние или вне доски
        """
        if not self.is_inside(a) or not self.is_inside(b):
            raise ValueError("Ячейки должны быть внутри доски")
        
        if not a.is_adjacent(b):
            raise ValueError("Ячейки должны быть соседними")
        
        tile_a = self.tile_at(a)
        tile_b = self.tile_at(b)
        
        self.set_tile(a, tile_b)
        self.set_tile(b, tile_a)
    
    def fill_empty(self, random) -> None:
        """Заполнить пустые ячейки новыми фишками.
        
        Args:
            random: Поставщик случайных фишек
        """
        for cell in self.enumerate_cells():
            if self.tile_at(cell) is None:
                tile_kind = random.next_tile_kind()
                self.set_tile(cell, Tile(tile_kind))
