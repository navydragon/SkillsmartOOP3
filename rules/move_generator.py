"""Генератор возможных ходов."""

from typing import List, Tuple

from board.board import Board
from board.cell import Cell
from .swap_validator import SwapValidator


class MoveGenerator:
    """Генератор всех возможных ходов."""
    
    def __init__(self):
        """Инициализировать генератор."""
        self._validator = SwapValidator()
    
    def generate_all_moves(self, board: Board) -> List[Tuple[Cell, Cell]]:
        """Сгенерировать все возможные ходы.
        
        Args:
            board: Доска для анализа
            
        Returns:
            List[Tuple[Cell, Cell]]: Список всех валидных ходов
        """
        moves = []
        
        # Проверяем все возможные пары соседних ячеек
        for cell in board.enumerate_cells():
            # Проверяем соседние ячейки
            neighbors = self._get_neighbors(cell, board)
            
            for neighbor in neighbors:
                if self._validator.is_valid_swap(board, cell, neighbor):
                    # Добавляем ход, если он ещё не добавлен
                    move = (cell, neighbor)
                    reverse_move = (neighbor, cell)
                    
                    if move not in moves and reverse_move not in moves:
                        moves.append(move)
        
        return moves
    
    def has_available_moves(self, board: Board) -> bool:
        """Проверить, есть ли доступные ходы.
        
        Args:
            board: Доска для проверки
            
        Returns:
            bool: True если есть доступные ходы
        """
        moves = self.generate_all_moves(board)
        return len(moves) > 0
    
    def _get_neighbors(self, cell: Cell, board: Board) -> List[Cell]:
        """Получить соседние ячейки.
        
        Args:
            cell: Исходная ячейка
            board: Доска для проверки границ
            
        Returns:
            List[Cell]: Список соседних ячеек
        """
        neighbors = []
        
        # Проверяем все четыре направления
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            neighbor = Cell(cell.row() + dx, cell.col() + dy)
            if board.is_inside(neighbor):
                neighbors.append(neighbor)
        
        return neighbors
