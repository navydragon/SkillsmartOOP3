"""Абстрактный базовый класс для игровой доски."""

from abc import ABC, abstractmethod
from typing import Optional, Iterable

from .tile import Tile
from .cell import Cell


class Board(ABC):
    """Абстрактная игровая доска."""
    
    @abstractmethod
    def width(self) -> int:
        """Получить ширину доски.
        
        Returns:
            int: Ширина доски
        """
        pass
    
    @abstractmethod
    def height(self) -> int:
        """Получить высоту доски.
        
        Returns:
            int: Высота доски
        """
        pass
    
    @abstractmethod
    def tile_at(self, cell: Cell) -> Optional[Tile]:
        """Получить фишку в указанной ячейке.
        
        Args:
            cell: Ячейка для проверки
            
        Returns:
            Optional[Tile]: Фишка в ячейке или None
        """
        pass
    
    def is_inside(self, cell: Cell) -> bool:
        """Проверить, находится ли ячейка в пределах доски.
        
        Args:
            cell: Ячейка для проверки
            
        Returns:
            bool: True если ячейка внутри доски
        """
        return (0 <= cell.row() < self.height() and 
                0 <= cell.col() < self.width())
    
    @abstractmethod
    def enumerate_cells(self) -> Iterable[Cell]:
        """Перечислить все ячейки доски.
        
        Returns:
            Iterable[Cell]: Все ячейки доски
        """
        pass
