"""Контейнер для управления зависимостями сервисов."""

from typing import Dict, Any


class ServiceContainer:
    """Контейнер для управления зависимостями сервисов."""
    
    def __init__(self):
        """Инициализировать пустой контейнер."""
        self._services: Dict[str, Any] = {}
    
    def register_swap_validator(self, validator) -> None:
        """Зарегистрировать валидатор свопов.
        
        Args:
            validator: Валидатор для проверки свопов
        """
        self._services['swap_validator'] = validator
    
    def register_match_finder(self, finder) -> None:
        """Зарегистрировать поисковик совпадений.
        
        Args:
            finder: Поисковик совпадений на доске
        """
        self._services['match_finder'] = finder
    
    def register_match_resolver(self, resolver) -> None:
        """Зарегистрировать резолвер совпадений.
        
        Args:
            resolver: Резолвер для удаления совпадений
        """
        self._services['match_resolver'] = resolver
    
    def register_gravity_engine(self, engine) -> None:
        """Зарегистрировать движок гравитации.
        
        Args:
            engine: Движок для падения и заполнения фишек
        """
        self._services['gravity_engine'] = engine
    
    def register_score_manager(self, manager) -> None:
        """Зарегистрировать менеджер счёта.
        
        Args:
            manager: Менеджер для расчёта и начисления очков
        """
        self._services['score_manager'] = manager
    
    def register_combo_tracker(self, tracker) -> None:
        """Зарегистрировать трекер комбо.
        
        Args:
            tracker: Трекер для отслеживания каскадов
        """
        self._services['combo_tracker'] = tracker
    
    def register_random_provider(self, provider) -> None:
        """Зарегистрировать поставщика случайностей.
        
        Args:
            provider: Поставщик случайных значений
        """
        self._services['random_provider'] = provider
    
    def register_move_generator(self, generator) -> None:
        """Зарегистрировать генератор ходов.
        
        Args:
            generator: Генератор возможных ходов
        """
        self._services['move_generator'] = generator
    
    def get_swap_validator(self):
        """Получить валидатор свопов.
        
        Returns:
            SwapValidator: Зарегистрированный валидатор
            
        Raises:
            KeyError: Если валидатор не зарегистрирован
        """
        return self._services['swap_validator']
    
    def get_match_finder(self):
        """Получить поисковик совпадений.
        
        Returns:
            MatchFinder: Зарегистрированный поисковик
            
        Raises:
            KeyError: Если поисковик не зарегистрирован
        """
        return self._services['match_finder']
    
    def get_match_resolver(self):
        """Получить резолвер совпадений.
        
        Returns:
            MatchResolver: Зарегистрированный резолвер
            
        Raises:
            KeyError: Если резолвер не зарегистрирован
        """
        return self._services['match_resolver']
    
    def get_gravity_engine(self):
        """Получить движок гравитации.
        
        Returns:
            GravityEngine: Зарегистрированный движок
            
        Raises:
            KeyError: Если движок не зарегистрирован
        """
        return self._services['gravity_engine']
    
    def get_score_manager(self):
        """Получить менеджер счёта.
        
        Returns:
            ScoreManager: Зарегистрированный менеджер
            
        Raises:
            KeyError: Если менеджер не зарегистрирован
        """
        return self._services['score_manager']
    
    def get_combo_tracker(self):
        """Получить трекер комбо.
        
        Returns:
            ComboTracker: Зарегистрированный трекер
            
        Raises:
            KeyError: Если трекер не зарегистрирован
        """
        return self._services['combo_tracker']
    
    def get_random_provider(self):
        """Получить поставщика случайностей.
        
        Returns:
            RandomProvider: Зарегистрированный поставщик
            
        Raises:
            KeyError: Если поставщик не зарегистрирован
        """
        return self._services['random_provider']
    
    def get_move_generator(self):
        """Получить генератор ходов.
        
        Returns:
            MoveGenerator: Зарегистрированный генератор
            
        Raises:
            KeyError: Если генератор не зарегистрирован
        """
        return self._services['move_generator']
    
    def get_services(self) -> Dict[str, Any]:
        """Получить все зарегистрированные сервисы.
        
        Returns:
            Dict[str, Any]: Словарь всех сервисов
        """
        return self._services.copy()
