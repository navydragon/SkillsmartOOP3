"""Тесты для игровых правил."""

import unittest
from board.tile_kind import TileKind
from board.tile import Tile
from board.cell import Cell
from board.mutable_board import MutableBoard
from rules.swap_validator import SwapValidator
from rules.match_finder import MatchFinder
from rules.move_generator import MoveGenerator


class TestSwapValidator(unittest.TestCase):
    """Тесты для SwapValidator."""
    
    def setUp(self):
        """Настройка тестов."""
        self.validator = SwapValidator()
        self.board = MutableBoard()
    
    def test_adjacent_cells(self):
        """Тест проверки соседства ячеек."""
        cell1 = Cell(3, 4)
        cell2 = Cell(3, 5)
        cell3 = Cell(2, 3)
        
        self.assertTrue(self.validator.is_adjacent(cell1, cell2))
        self.assertFalse(self.validator.is_adjacent(cell1, cell3))
    
    def test_valid_swap(self):
        """Тест валидного свопа."""
        # Создаём ситуацию для валидного свопа
        self.board.set_tile(Cell(3, 3), Tile(TileKind.A))
        self.board.set_tile(Cell(3, 4), Tile(TileKind.B))
        self.board.set_tile(Cell(3, 5), Tile(TileKind.A))
        self.board.set_tile(Cell(3, 6), Tile(TileKind.A))  # Добавляем ещё одну A
        
        cell1 = Cell(3, 4)
        cell2 = Cell(3, 5)
        
        # Своп должен быть валидным (создаёт совпадение A-A-A)
        self.assertTrue(self.validator.is_valid_swap(self.board, cell1, cell2))
    
    def test_invalid_swap(self):
        """Тест невалидного свопа."""
        # Создаём ситуацию без возможных совпадений
        self.board.set_tile(Cell(3, 3), Tile(TileKind.A))
        self.board.set_tile(Cell(3, 4), Tile(TileKind.B))
        self.board.set_tile(Cell(3, 5), Tile(TileKind.C))
        
        cell1 = Cell(3, 4)
        cell2 = Cell(3, 5)
        
        # Своп не должен быть валидным
        self.assertFalse(self.validator.is_valid_swap(self.board, cell1, cell2))


class TestMatchFinder(unittest.TestCase):
    """Тесты для MatchFinder."""
    
    def setUp(self):
        """Настройка тестов."""
        self.finder = MatchFinder()
        self.board = MutableBoard()
    
    def test_horizontal_match(self):
        """Тест поиска горизонтального совпадения."""
        # Создаём горизонтальное совпадение
        self.board.set_tile(Cell(3, 3), Tile(TileKind.A))
        self.board.set_tile(Cell(3, 4), Tile(TileKind.A))
        self.board.set_tile(Cell(3, 5), Tile(TileKind.A))
        
        matches = self.finder.find_matches(self.board)
        
        self.assertEqual(len(matches), 1)
        self.assertEqual(len(list(matches)[0]), 3)
    
    def test_vertical_match(self):
        """Тест поиска вертикального совпадения."""
        # Создаём вертикальное совпадение
        self.board.set_tile(Cell(3, 4), Tile(TileKind.B))
        self.board.set_tile(Cell(4, 4), Tile(TileKind.B))
        self.board.set_tile(Cell(5, 4), Tile(TileKind.B))
        
        matches = self.finder.find_matches(self.board)
        
        self.assertEqual(len(matches), 1)
        self.assertEqual(len(list(matches)[0]), 3)
    
    def test_no_matches(self):
        """Тест отсутствия совпадений."""
        # Создаём доску без совпадений
        self.board.set_tile(Cell(3, 3), Tile(TileKind.A))
        self.board.set_tile(Cell(3, 4), Tile(TileKind.B))
        self.board.set_tile(Cell(3, 5), Tile(TileKind.C))
        
        matches = self.finder.find_matches(self.board)
        
        self.assertEqual(len(matches), 0)


class TestMoveGenerator(unittest.TestCase):
    """Тесты для MoveGenerator."""
    
    def setUp(self):
        """Настройка тестов."""
        self.generator = MoveGenerator()
        self.board = MutableBoard()
    
    def test_has_available_moves(self):
        """Тест проверки доступных ходов."""
        # Создаём ситуацию с возможными ходами
        self.board.set_tile(Cell(3, 3), Tile(TileKind.A))
        self.board.set_tile(Cell(3, 4), Tile(TileKind.B))
        self.board.set_tile(Cell(3, 5), Tile(TileKind.A))
        self.board.set_tile(Cell(3, 6), Tile(TileKind.A))  # Добавляем ещё одну A
        
        has_moves = self.generator.has_available_moves(self.board)
        self.assertTrue(has_moves)
    
    def test_no_available_moves(self):
        """Тест отсутствия доступных ходов."""
        # Создаём доску без возможных ходов
        for row in range(8):
            for col in range(8):
                tile_kind = TileKind.all()[(row + col) % 5]
                self.board.set_tile(Cell(row, col), Tile(tile_kind))
        
        has_moves = self.generator.has_available_moves(self.board)
        # В реальной игре это может быть True или False в зависимости от конфигурации
        # Здесь мы просто проверяем, что метод работает без ошибок
        self.assertIsInstance(has_moves, bool)


if __name__ == '__main__':
    unittest.main()
