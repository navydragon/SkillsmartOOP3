"""Тесты для игровой механики."""

import unittest
from board.tile_kind import TileKind
from board.tile import Tile
from board.cell import Cell
from board.mutable_board import MutableBoard
from mechanics.match_resolver import MatchResolver
from mechanics.gravity_engine import GravityEngine
from random_generator.random_provider_default import RandomProviderDefault


class TestMatchResolver(unittest.TestCase):
    """Тесты для MatchResolver."""
    
    def setUp(self):
        """Настройка тестов."""
        self.resolver = MatchResolver()
        self.board = MutableBoard()
    
    def test_remove_matches(self):
        """Тест удаления совпадений."""
        # Создаём совпадение
        match_cells = {Cell(3, 3), Cell(3, 4), Cell(3, 5)}
        for cell in match_cells:
            self.board.set_tile(cell, Tile(TileKind.A))
        
        matches = {frozenset(match_cells)}
        removed_count = self.resolver.remove_matches(self.board, matches)
        
        self.assertEqual(removed_count, 3)
        
        # Проверяем, что ячейки очищены
        for cell in match_cells:
            self.assertIsNone(self.board.tile_at(cell))
    
    def test_remove_multiple_matches(self):
        """Тест удаления нескольких совпадений."""
        # Создаём два совпадения
        match1 = {Cell(3, 3), Cell(3, 4), Cell(3, 5)}
        match2 = {Cell(4, 3), Cell(4, 4), Cell(4, 5)}
        
        for cell in match1:
            self.board.set_tile(cell, Tile(TileKind.A))
        for cell in match2:
            self.board.set_tile(cell, Tile(TileKind.B))
        
        matches = {frozenset(match1), frozenset(match2)}
        removed_count = self.resolver.remove_matches(self.board, matches)
        
        self.assertEqual(removed_count, 6)
        
        # Проверяем, что все ячейки очищены
        for cell in match1.union(match2):
            self.assertIsNone(self.board.tile_at(cell))


class TestGravityEngine(unittest.TestCase):
    """Тесты для GravityEngine."""
    
    def setUp(self):
        """Настройка тестов."""
        self.engine = GravityEngine()
        self.board = MutableBoard()
        self.random_provider = RandomProviderDefault(42)
    
    def test_apply_gravity(self):
        """Тест применения гравитации."""
        # Создаём столбец с "дыркой" посередине
        self.board.set_tile(Cell(0, 3), Tile(TileKind.A))
        self.board.set_tile(Cell(1, 3), Tile(TileKind.B))
        # Ячейка (2, 3) пустая
        self.board.set_tile(Cell(3, 3), Tile(TileKind.C))
        self.board.set_tile(Cell(4, 3), Tile(TileKind.D))
        
        self.engine.apply_gravity(self.board)
        
        # Проверяем, что фишки "упали" вниз
        self.assertEqual(self.board.tile_at(Cell(0, 3)).kind(), TileKind.A)
        self.assertEqual(self.board.tile_at(Cell(1, 3)).kind(), TileKind.B)
        self.assertEqual(self.board.tile_at(Cell(2, 3)).kind(), TileKind.C)
        self.assertEqual(self.board.tile_at(Cell(3, 3)).kind(), TileKind.D)
        self.assertIsNone(self.board.tile_at(Cell(4, 3)))
    
    def test_refill(self):
        """Тест заполнения пустых ячеек."""
        # Очищаем несколько ячеек
        self.board.set_tile(Cell(3, 3), None)
        self.board.set_tile(Cell(3, 4), None)
        
        self.engine.refill(self.board, self.random_provider)
        
        # Проверяем, что ячейки заполнены
        self.assertIsNotNone(self.board.tile_at(Cell(3, 3)))
        self.assertIsNotNone(self.board.tile_at(Cell(3, 4)))
        
        # Проверяем, что фишки валидного типа
        tile1 = self.board.tile_at(Cell(3, 3))
        tile2 = self.board.tile_at(Cell(3, 4))
        self.assertIn(tile1.kind(), TileKind.all())
        self.assertIn(tile2.kind(), TileKind.all())


if __name__ == '__main__':
    unittest.main()
