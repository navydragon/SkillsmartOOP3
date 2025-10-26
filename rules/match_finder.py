"""Поисковик совпадений на доске."""

from typing import Set, Tuple

from board.board import Board
from board.cell import Cell
from board.tile import Tile


class MatchFinder:
    """Поисковик совпадений на доске."""
    
    def find_matches(self, board: Board) -> Set[Set[Cell]]:
        """Найти все совпадения на доске.
        
        Args:
            board: Доска для поиска совпадений
            
        Returns:
            Set[Set[Cell]]: Множество групп ячеек с совпадениями
            
        Note:
            Каждая группа содержит ≥3 ячейки одного типа в ряд
        """
        horizontal_matches = self.find_horizontal_matches(board)
        vertical_matches = self.find_vertical_matches(board)
        
        # Объединяем все совпадения
        all_matches = horizontal_matches.union(vertical_matches)
        
        # Убираем пересечения между группами
        return self._remove_overlapping_matches(all_matches)
    
    def find_horizontal_matches(self, board: Board) -> Set[Set[Cell]]:
        """Найти горизонтальные совпадения.
        
        Args:
            board: Доска для поиска
            
        Returns:
            Set[Set[Cell]]: Горизонтальные группы совпадений
        """
        matches = set()
        
        for row in range(board.height()):
            col = 0
            while col < board.width():
                match_cells = self._find_matches_in_line(
                    board, Cell(row, col), (0, 1)
                )
                if len(match_cells) >= 3:
                    matches.add(frozenset(match_cells))
                    col += len(match_cells)
                else:
                    col += 1
        
        return {frozenset(match) for match in matches}
    
    def find_vertical_matches(self, board: Board) -> Set[Set[Cell]]:
        """Найти вертикальные совпадения.
        
        Args:
            board: Доска для поиска
            
        Returns:
            Set[Set[Cell]]: Вертикальные группы совпадений
        """
        matches = set()
        
        for col in range(board.width()):
            row = 0
            while row < board.height():
                match_cells = self._find_matches_in_line(
                    board, Cell(row, col), (1, 0)
                )
                if len(match_cells) >= 3:
                    matches.add(frozenset(match_cells))
                    row += len(match_cells)
                else:
                    row += 1
        
        return {frozenset(match) for match in matches}
    
    def _find_matches_in_line(self, board: Board, start: Cell, direction: Tuple[int, int]) -> Set[Cell]:
        """Найти совпадения в заданном направлении.
        
        Args:
            board: Доска для поиска
            start: Начальная ячейка
            direction: Направление поиска (dx, dy)
            
        Returns:
            Set[Cell]: Ячейки с совпадением в направлении
        """
        start_tile = board.tile_at(start)
        if start_tile is None:
            return set()
        
        match_cells = {start}
        dx, dy = direction
        
        # Проверяем в положительном направлении
        current = Cell(start.row() + dx, start.col() + dy)
        while board.is_inside(current):
            current_tile = board.tile_at(current)
            if current_tile is not None and current_tile.kind() == start_tile.kind():
                match_cells.add(current)
                current = Cell(current.row() + dx, current.col() + dy)
            else:
                break
        
        return match_cells
    
    def _remove_overlapping_matches(self, matches: Set[Set[Cell]]) -> Set[Set[Cell]]:
        """Убрать пересекающиеся совпадения.
        
        Args:
            matches: Множество групп совпадений
            
        Returns:
            Set[Set[Cell]]: Группы без пересечений
        """
        if not matches:
            return matches
        
        # Сортируем группы по размеру (большие сначала)
        sorted_matches = sorted(matches, key=len, reverse=True)
        
        result = set()
        used_cells = set()
        
        for match_group in sorted_matches:
            # Проверяем, есть ли пересечения с уже выбранными группами
            if not match_group.intersection(used_cells):
                result.add(match_group)
                used_cells.update(match_group)
        
        return result
