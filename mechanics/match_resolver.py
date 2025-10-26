"""Резолвер для удаления совпадений."""

from typing import Set

from board.mutable_board import MutableBoard
from board.cell import Cell


class MatchResolver:
    """Резолвер для удаления совпадений."""
    
    def remove_matches(self, board: MutableBoard, matches: Set[Set[Cell]]) -> int:
        """Удалить совпадения с доски.
        
        Args:
            board: Доска для изменения
            matches: Группы ячеек для удаления
            
        Returns:
            int: Количество удалённых фишек
            
        Raises:
            ValueError: Если группы совпадений невалидны
        """
        self._validate_match_groups(board, matches)
        
        total_removed = 0
        
        for group in matches:
            removed_count = self._remove_group(board, group)
            total_removed += removed_count
        
        return total_removed
    
    def _validate_match_groups(self, board: MutableBoard, matches: Set[Set[Cell]]) -> None:
        """Валидировать группы совпадений.
        
        Args:
            board: Доска для проверки
            matches: Группы для валидации
            
        Raises:
            ValueError: Если группы невалидны
        """
        for group in matches:
            if len(group) < 3:
                raise ValueError("Группа совпадений должна содержать минимум 3 ячейки")
            
            for cell in group:
                if not board.is_inside(cell):
                    raise ValueError(f"Ячейка {cell} вне доски")
                
                if board.tile_at(cell) is None:
                    raise ValueError(f"Ячейка {cell} пуста")
    
    def _remove_group(self, board: MutableBoard, group: Set[Cell]) -> int:
        """Удалить одну группу совпадений.
        
        Args:
            board: Доска для изменения
            group: Группа ячеек для удаления
            
        Returns:
            int: Количество удалённых фишек
        """
        removed_count = 0
        
        for cell in group:
            if board.tile_at(cell) is not None:
                board.set_tile(cell, None)
                removed_count += 1
        
        return removed_count
