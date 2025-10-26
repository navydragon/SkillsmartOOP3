"""Движок гравитации и заполнения."""

from typing import List, Optional

from board.mutable_board import MutableBoard
from board.tile import Tile


class GravityEngine:
    """Движок гравитации и заполнения."""
    
    def apply_gravity(self, board: MutableBoard) -> None:
        """Применить гравитацию ко всем столбцам.
        
        Args:
            board: Доска для обработки
            
        Note:
            Фишки падают вниз, сохраняя относительный порядок
        """
        for col in range(board.width()):
            self._apply_gravity_to_column(board, col)
    
    def refill(self, board: MutableBoard, random) -> None:
        """Заполнить пустые ячейки новыми фишками.
        
        Args:
            board: Доска для заполнения
            random: Поставщик случайных фишек
        """
        for col in range(board.width()):
            for row in range(board.height()):
                from board.cell import Cell
                cell = Cell(row, col)
                if board.tile_at(cell) is None:
                    tile_kind = random.next_tile_kind()
                    board.set_tile(cell, Tile(tile_kind))
    
    def _apply_gravity_to_column(self, board: MutableBoard, col: int) -> None:
        """Применить гравитацию к одному столбцу.
        
        Args:
            board: Доска для изменения
            col: Индекс столбца
        """
        # Собираем все фишки в столбце
        column_tiles = []
        for row in range(board.height()):
            from board.cell import Cell
            cell = Cell(row, col)
            tile = board.tile_at(cell)
            column_tiles.append(tile)
        
        # Сжимаем столбец (убираем None между фишками)
        compacted_tiles = self._compact_column(column_tiles)
        
        # Заполняем столбец сжатыми фишками
        for row in range(board.height()):
            from board.cell import Cell
            cell = Cell(row, col)
            board.set_tile(cell, compacted_tiles[row])
    
    def _compact_column(self, tiles: List[Optional[Tile]]) -> List[Optional[Tile]]:
        """Сжать столбец, убрав None между фишками.
        
        Args:
            tiles: Список фишек столбца
            
        Returns:
            List[Optional[Tile]]: Сжатый столбец
        """
        # Собираем все не-None фишки
        non_none_tiles = [tile for tile in tiles if tile is not None]
        
        # Создаём новый список, заполняя None сверху
        result = [None] * len(tiles)
        
        # Размещаем фишки снизу
        start_index = len(tiles) - len(non_none_tiles)
        for i, tile in enumerate(non_none_tiles):
            result[start_index + i] = tile
        
        return result
