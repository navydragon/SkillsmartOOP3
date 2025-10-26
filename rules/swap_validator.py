"""Валидатор для проверки допустимости свопов."""

from typing import Set

from board.board import Board
from board.cell import Cell
from board.tile import Tile


class SwapValidator:
    """Валидатор для проверки допустимости свопов."""
    
    def is_adjacent(self, a: Cell, b: Cell) -> bool:
        """Проверить, являются ли ячейки соседними.
        
        Args:
            a: Первая ячейка
            b: Вторая ячейка
            
        Returns:
            bool: True если ячейки соседние по стороне
        """
        return a.is_adjacent(b)
    
    def is_swap_creating_match(self, board: Board, a: Cell, b: Cell) -> bool:
        """Проверить, создаёт ли своп совпадения.
        
        Args:
            board: Доска для проверки
            a: Первая ячейка свопа
            b: Вторая ячейка свопа
            
        Returns:
            bool: True если своп создаст ≥1 совпадение
            
        Raises:
            ValueError: Если ячейки не соседние или вне доски
        """
        if not self.is_adjacent(a, b):
            raise ValueError("Ячейки не являются соседними")
        
        if not board.is_inside(a) or not board.is_inside(b):
            raise ValueError("Ячейки вне доски")
        
        # Симулируем своп
        simulated_board = self._simulate_swap(board, a, b)
        
        # Проверяем наличие совпадений после свопа
        from .match_finder import MatchFinder
        match_finder = MatchFinder()
        matches = match_finder.find_matches(simulated_board)
        
        return len(matches) > 0
    
    def is_valid_swap(self, board: Board, a: Cell, b: Cell) -> bool:
        """Проверить валидность свопа.
        
        Args:
            board: Доска для проверки
            a: Первая ячейка
            b: Вторая ячейка
            
        Returns:
            bool: True если своп валиден
        """
        try:
            return (self.is_adjacent(a, b) and 
                   board.is_inside(a) and 
                   board.is_inside(b) and
                   self.is_swap_creating_match(board, a, b))
        except ValueError:
            return False
    
    def _simulate_swap(self, board: Board, a: Cell, b: Cell) -> Board:
        """Симулировать своп на копии доски.
        
        Args:
            board: Исходная доска
            a: Первая ячейка
            b: Вторая ячейка
            
        Returns:
            Board: Доска после симуляции свопа
        """
        # Создаём копию доски
        if hasattr(board, 'clone'):
            simulated = board.clone()
        else:
            # Если нет метода clone, создаём новую доску и копируем содержимое
            from board.mutable_board import MutableBoard
            simulated = MutableBoard()
            for cell in board.enumerate_cells():
                tile = board.tile_at(cell)
                if tile is not None:
                    simulated.set_tile(cell, Tile(tile.kind()))
        
        # Выполняем своп на копии
        tile_a = simulated.tile_at(a)
        tile_b = simulated.tile_at(b)
        simulated.set_tile(a, tile_b)
        simulated.set_tile(b, tile_a)
        
        return simulated
