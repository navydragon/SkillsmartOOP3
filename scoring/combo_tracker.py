"""Трекер для отслеживания каскадов."""


class ComboTracker:
    """Трекер для отслеживания каскадов."""
    
    def __init__(self, initial_index: int = 0):
        """Инициализировать трекер.
        
        Args:
            initial_index: Начальный индекс каскада
        """
        self._current_index = initial_index
    
    def reset(self) -> None:
        """Сбросить индекс каскада к 0."""
        self._current_index = 0
    
    def increment(self) -> None:
        """Увеличить индекс каскада на 1."""
        self._current_index += 1
    
    def current_index(self) -> int:
        """Получить текущий индекс каскада.
        
        Returns:
            int: Текущий индекс каскада
        """
        return self._current_index
    
    def set_index(self, index: int) -> None:
        """Установить индекс каскада.
        
        Args:
            index: Новый индекс (≥0)
        """
        if index < 0:
            raise ValueError("Индекс каскада не может быть отрицательным")
        
        self._current_index = index
