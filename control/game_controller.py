"""Основной контроллер игровой логики."""

from board.cell import Cell
from board.mutable_board import MutableBoard
from .game_state import GameState


class GameController:
    """Основной контроллер игровой логики."""
    
    def __init__(self, services):
        """Инициализировать контроллер с сервисами.
        
        Args:
            services: Контейнер с игровыми сервисами
        """
        self._services = services
        self._swap_validator = services.get_swap_validator()
        self._match_finder = services.get_match_finder()
        self._match_resolver = services.get_match_resolver()
        self._gravity_engine = services.get_gravity_engine()
        self._score_manager = services.get_score_manager()
        self._combo_tracker = services.get_combo_tracker()
        self._random_provider = services.get_random_provider()
    
    def perform_move(self, state: GameState, a: Cell, b: Cell) -> bool:
        """Выполнить ход игрока.
        
        Args:
            state: Текущее состояние игры
            a: Первая ячейка для свопа
            b: Вторая ячейка для свопа
            
        Returns:
            bool: True если ход выполнен успешно, False если невалидный
            
        Raises:
            ValueError: Если ячейки не соседние или вне доски
        """
        # Проверяем валидность свопа
        if not self._swap_validator.is_valid_swap(state.board, a, b):
            return False
        
        # Создаём изменяемую копию доски
        mutable_board = state.board.clone()
        
        # Выполняем своп
        mutable_board.swap(a, b)
        
        # Выполняем каскадное разрешение совпадений
        total_points = self._execute_cascade(mutable_board, state)
        
        # Обновляем состояние
        state.board = mutable_board
        state.add_score(total_points)
        
        return True
    
    def update_moves_available(self, state: GameState) -> None:
        """Обновить флаг доступности ходов.
        
        Args:
            state: Состояние для обновления
        """
        move_generator = self._services.get_move_generator()
        has_moves = move_generator.has_available_moves(state.board)
        state.set_moves_available(has_moves)
    
    def is_game_over(self, state: GameState) -> bool:
        """Проверить, завершена ли игра.
        
        Args:
            state: Состояние для проверки
            
        Returns:
            bool: True если игра завершена
        """
        return not state.has_moves()
    
    def _execute_cascade(self, board: MutableBoard, state: GameState) -> int:
        """Выполнить каскадное разрешение совпадений.
        
        Args:
            board: Доска для обработки
            state: Состояние для обновления счёта
            
        Returns:
            int: Общее количество очков за каскад
        """
        self._combo_tracker.reset()
        total_points = 0
        
        while True:
            # Ищем совпадения
            matches = self._match_finder.find_matches(board)
            
            if len(matches) == 0:
                break
            
            # Удаляем совпадения
            removed_count = self._match_resolver.remove_matches(board, matches)
            
            # Начисляем очки
            cascade_index = self._combo_tracker.current_index()
            points = self._score_manager.score_for_removed(removed_count, cascade_index)
            total_points += points
            
            # Применяем гравитацию
            self._gravity_engine.apply_gravity(board)
            
            # Заполняем пустые ячейки
            self._gravity_engine.refill(board, self._random_provider)
            
            # Увеличиваем индекс каскада
            self._combo_tracker.increment()
        
        return total_points
