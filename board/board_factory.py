"""Фабрика для создания игровых досок."""

from .board import Board
from .mutable_board import MutableBoard


class BoardFactory:
    """Фабрика для создания различных типов досок."""
    
    @staticmethod
    def create_empty_board() -> MutableBoard:
        """Создать пустую доску 8x8.
        
        Returns:
            MutableBoard: Пустая доска с None во всех ячейках
        """
        return MutableBoard()
    
    @staticmethod
    def create_initial_board(random) -> MutableBoard:
        """Создать доску с случайными фишками.
        
        Args:
            random: Источник случайных значений
            
        Returns:
            MutableBoard: Доска, заполненная случайными фишками A-E
        """
        board = MutableBoard()
        board.fill_empty(random)
        return board
    
    @staticmethod
    def create_board_without_matches(random, match_finder) -> MutableBoard:
        """Создать доску без начальных совпадений.
        
        Args:
            random: Источник случайных значений
            match_finder: Поисковик совпадений
            
        Returns:
            MutableBoard: Доска без совпадений ≥3 в ряд
            
        Note:
            Может потребовать несколько попыток генерации
        """
        max_attempts = 100
        
        for attempt in range(max_attempts):
            board = BoardFactory.create_initial_board(random)
            matches = match_finder.find_matches(board)
            
            if len(matches) == 0:
                return board
        
        # Если не удалось создать доску без совпадений, возвращаем последнюю попытку
        return board
