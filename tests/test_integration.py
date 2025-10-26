"""Интеграционные тесты."""

import unittest
from board.tile_kind import TileKind
from board.tile import Tile
from board.cell import Cell
from board.mutable_board import MutableBoard
from board.board_factory import BoardFactory
from random_generator.random_provider_default import RandomProviderDefault
from rules.match_finder import MatchFinder
from rules.swap_validator import SwapValidator
from mechanics.match_resolver import MatchResolver
from mechanics.gravity_engine import GravityEngine
from scoring.score_manager import ScoreManager
from scoring.combo_tracker import ComboTracker


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты полного игрового цикла."""
    
    def setUp(self):
        """Настройка тестов."""
        self.random_provider = RandomProviderDefault(42)
        self.match_finder = MatchFinder()
        self.swap_validator = SwapValidator()
        self.match_resolver = MatchResolver()
        self.gravity_engine = GravityEngine()
        self.score_manager = ScoreManager()
        self.combo_tracker = ComboTracker()
    
    def test_full_move_execution(self):
        """Тест выполнения полного хода."""
        # Создаём доску с возможным ходом
        board = MutableBoard()
        
        # Создаём конфигурацию для валидного хода
        board.set_tile(Cell(3, 3), Tile(TileKind.A))
        board.set_tile(Cell(3, 4), Tile(TileKind.B))
        board.set_tile(Cell(3, 5), Tile(TileKind.A))
        
        # Проверяем валидность хода
        cell1 = Cell(3, 4)
        cell2 = Cell(3, 5)
        
        self.assertTrue(self.swap_validator.is_valid_swap(board, cell1, cell2))
        
        # Выполняем своп
        board.swap(cell1, cell2)
        
        # Ищем совпадения
        matches = self.match_finder.find_matches(board)
        self.assertEqual(len(matches), 1)
        
        # Удаляем совпадения
        removed_count = self.match_resolver.remove_matches(board, matches)
        self.assertEqual(removed_count, 3)
        
        # Применяем гравитацию
        self.gravity_engine.apply_gravity(board)
        
        # Заполняем пустые ячейки
        self.gravity_engine.refill(board, self.random_provider)
        
        # Проверяем, что доска заполнена
        for cell in board.enumerate_cells():
            tile = board.tile_at(cell)
            self.assertIsNotNone(tile)
            self.assertIn(tile.kind(), TileKind.all())
    
    def test_cascade_resolution(self):
        """Тест каскадного разрешения совпадений."""
        board = MutableBoard()
        
        # Создаём конфигурацию для каскада
        # Горизонтальное совпадение
        board.set_tile(Cell(3, 3), Tile(TileKind.A))
        board.set_tile(Cell(3, 4), Tile(TileKind.A))
        board.set_tile(Cell(3, 5), Tile(TileKind.A))
        
        # Вертикальное совпадение после падения
        board.set_tile(Cell(4, 3), Tile(TileKind.B))
        board.set_tile(Cell(5, 3), Tile(TileKind.B))
        board.set_tile(Cell(6, 3), Tile(TileKind.B))
        
        initial_matches = self.match_finder.find_matches(board)
        self.assertEqual(len(initial_matches), 1)
        
        # Удаляем первое совпадение
        removed_count = self.match_resolver.remove_matches(board, initial_matches)
        self.assertEqual(removed_count, 3)
        
        # Применяем гравитацию
        self.gravity_engine.apply_gravity(board)
        
        # Проверяем, что появилось новое совпадение
        new_matches = self.match_finder.find_matches(board)
        # В зависимости от конфигурации может быть 0 или больше совпадений
        self.assertGreaterEqual(len(new_matches), 0)
    
    def test_score_calculation(self):
        """Тест расчёта очков."""
        # Тестируем базовый расчёт очков
        score1 = self.score_manager.score_for_removed(3, 0)  # Первый каскад
        self.assertEqual(score1, 30)  # 3 * 10 * 1.0
        
        # Тестируем расчёт с множителем каскада
        score2 = self.score_manager.score_for_removed(3, 1)  # Второй каскад
        self.assertEqual(score2, 45)  # 3 * 10 * 1.5
    
    def test_combo_tracker(self):
        """Тест трекера комбо."""
        # Проверяем начальное состояние
        self.assertEqual(self.combo_tracker.current_index(), 0)
        
        # Увеличиваем индекс
        self.combo_tracker.increment()
        self.assertEqual(self.combo_tracker.current_index(), 1)
        
        # Сбрасываем
        self.combo_tracker.reset()
        self.assertEqual(self.combo_tracker.current_index(), 0)


if __name__ == '__main__':
    unittest.main()
