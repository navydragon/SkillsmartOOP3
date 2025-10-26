"""Состояние игры."""

from dataclasses import dataclass
from typing import Optional

from board.board import Board


@dataclass
class GameState:
    """Состояние игры."""
    
    board: Board
    score: int
    moves_available: bool
    
    def __post_init__(self):
        """Валидация после инициализации."""
        if self.score < 0:
            raise ValueError("Счёт не может быть отрицательным")
        if self.board is None:
            raise ValueError("Доска обязательна")
    
    def get_score(self) -> int:
        """Получить текущий счёт.
        
        Returns:
            int: Текущий счёт игрока
        """
        return self.score
    
    def add_score(self, points: int) -> None:
        """Добавить очки к счёту.
        
        Args:
            points: Количество очков для добавления (≥0)
        """
        if points < 0:
            raise ValueError("Очки не могут быть отрицательными")
        
        self.score += points
    
    def has_moves(self) -> bool:
        """Проверить, есть ли доступные ходы.
        
        Returns:
            bool: True если есть доступные ходы
        """
        return self.moves_available
    
    def set_moves_available(self, available: bool) -> None:
        """Установить флаг доступности ходов.
        
        Args:
            available: Доступны ли ходы
        """
        self.moves_available = available
