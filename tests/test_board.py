"""Тесты для игровой доски."""

import unittest
from board.tile_kind import TileKind
from board.tile import Tile
from board.cell import Cell
from board.mutable_board import MutableBoard
from board.board_factory import BoardFactory
from random_generator.random_provider_default import RandomProviderDefault


class TestTileKind(unittest.TestCase):
    """Тесты для TileKind."""
    
    def test_all_types(self):
        """Тест получения всех типов фишек."""
        all_types = TileKind.all()
        self.assertEqual(len(all_types), 5)
        self.assertIn(TileKind.A, all_types)
        self.assertIn(TileKind.B, all_types)
        self.assertIn(TileKind.C, all_types)
        self.assertIn(TileKind.D, all_types)
        self.assertIn(TileKind.E, all_types)


class TestTile(unittest.TestCase):
    """Тесты для Tile."""
    
    def test_tile_creation(self):
        """Тест создания фишки."""
        tile = Tile(TileKind.A)
        self.assertEqual(tile.kind(), TileKind.A)
    
    def test_tile_equality(self):
        """Тест равенства фишек."""
        tile1 = Tile(TileKind.A)
        tile2 = Tile(TileKind.A)
        tile3 = Tile(TileKind.B)
        
        self.assertEqual(tile1, tile2)
        self.assertNotEqual(tile1, tile3)
    
    def test_tile_string_representation(self):
        """Тест строкового представления фишки."""
        tile = Tile(TileKind.A)
        self.assertEqual(str(tile), "A")


class TestCell(unittest.TestCase):
    """Тесты для Cell."""
    
    def test_cell_creation(self):
        """Тест создания ячейки."""
        cell = Cell(3, 4)
        self.assertEqual(cell.row(), 3)
        self.assertEqual(cell.col(), 4)
    
    def test_cell_validity(self):
        """Тест валидности ячейки."""
        valid_cell = Cell(3, 4)
        invalid_cell1 = Cell(-1, 4)
        invalid_cell2 = Cell(3, 8)
        
        self.assertTrue(valid_cell.is_valid())
        self.assertFalse(invalid_cell1.is_valid())
        self.assertFalse(invalid_cell2.is_valid())
    
    def test_cell_adjacency(self):
        """Тест соседства ячеек."""
        cell = Cell(3, 4)
        adjacent_cells = [
            Cell(2, 4),  # сверху
            Cell(4, 4),  # снизу
            Cell(3, 3),  # слева
            Cell(3, 5),  # справа
        ]
        non_adjacent_cells = [
            Cell(2, 3),  # диагональ
            Cell(1, 4),   # далеко
            Cell(3, 6),   # далеко
        ]
        
        for adj_cell in adjacent_cells:
            self.assertTrue(cell.is_adjacent(adj_cell))
        
        for non_adj_cell in non_adjacent_cells:
            self.assertFalse(cell.is_adjacent(non_adj_cell))


class TestMutableBoard(unittest.TestCase):
    """Тесты для MutableBoard."""
    
    def setUp(self):
        """Настройка тестов."""
        self.board = MutableBoard()
    
    def test_board_dimensions(self):
        """Тест размеров доски."""
        self.assertEqual(self.board.width(), 8)
        self.assertEqual(self.board.height(), 8)
    
    def test_empty_board(self):
        """Тест пустой доски."""
        for cell in self.board.enumerate_cells():
            self.assertIsNone(self.board.tile_at(cell))
    
    def test_set_tile(self):
        """Тест установки фишки."""
        cell = Cell(3, 4)
        tile = Tile(TileKind.A)
        
        self.board.set_tile(cell, tile)
        self.assertEqual(self.board.tile_at(cell), tile)
    
    def test_swap_tiles(self):
        """Тест обмена фишек."""
        cell1 = Cell(3, 4)
        cell2 = Cell(3, 5)
        tile1 = Tile(TileKind.A)
        tile2 = Tile(TileKind.B)
        
        self.board.set_tile(cell1, tile1)
        self.board.set_tile(cell2, tile2)
        
        self.board.swap(cell1, cell2)
        
        self.assertEqual(self.board.tile_at(cell1), tile2)
        self.assertEqual(self.board.tile_at(cell2), tile1)
    
    def test_fill_empty(self):
        """Тест заполнения пустых ячеек."""
        random_provider = RandomProviderDefault(42)  # Фиксированный seed для воспроизводимости
        
        self.board.fill_empty(random_provider)
        
        for cell in self.board.enumerate_cells():
            tile = self.board.tile_at(cell)
            self.assertIsNotNone(tile)
            self.assertIn(tile.kind(), TileKind.all())


class TestBoardFactory(unittest.TestCase):
    """Тесты для BoardFactory."""
    
    def test_create_empty_board(self):
        """Тест создания пустой доски."""
        board = BoardFactory.create_empty_board()
        
        self.assertIsInstance(board, MutableBoard)
        for cell in board.enumerate_cells():
            self.assertIsNone(board.tile_at(cell))
    
    def test_create_initial_board(self):
        """Тест создания доски с фишками."""
        random_provider = RandomProviderDefault(42)
        board = BoardFactory.create_initial_board(random_provider)
        
        self.assertIsInstance(board, MutableBoard)
        for cell in board.enumerate_cells():
            tile = board.tile_at(cell)
            self.assertIsNotNone(tile)
            self.assertIn(tile.kind(), TileKind.all())


if __name__ == '__main__':
    unittest.main()
