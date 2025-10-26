"""Builder для создания GameState."""

from typing import Optional

from .game_state import GameState
from board.board import Board


class GameStateBuilder:
    """Builder для создания GameState с гибкой конфигурацией."""
    
    def __init__(self):
        """Инициализировать builder с значениями по умолчанию."""
        self._board: Optional[Board] = None
        self._score: int = 0
        self._moves_available: bool = True
    
    def with_board(self, board: Board) -> 'GameStateBuilder':
        """Установить доску.
        
        Args:
            board: Игровая доска
            
        Returns:
            GameStateBuilder: self для цепочки вызовов
        """
        self._board = board
        return self
    
    def with_score(self, score: int) -> 'GameStateBuilder':
        """Установить счёт.
        
        Args:
            score: Начальный счёт (≥0)
            
        Returns:
            GameStateBuilder: self для цепочки вызовов
        """
        self._score = score
        return self
    
    def with_moves_available(self, available: bool) -> 'GameStateBuilder':
        """Установить доступность ходов.
        
        Args:
            available: Есть ли доступные ходы
            
        Returns:
            GameStateBuilder: self для цепочки вызовов
        """
        self._moves_available = available
        return self
    
    def build(self) -> GameState:
        """Создать GameState.
        
        Returns:
            GameState: Сконфигурированное состояние игры
            
        Raises:
            ValueError: Если не установлена доска
        """
        if self._board is None:
            raise ValueError("Доска обязательна для создания GameState")
        
        return GameState(
            board=self._board,
            score=self._score,
            moves_available=self._moves_available
        )
