"""Менеджер для расчёта и начисления очков."""


class ScoreManager:
    """Менеджер для расчёта и начисления очков."""
    
    def __init__(self, base_points: int = 10, cascade_multiplier: float = 1.5):
        """Инициализировать менеджер счёта.
        
        Args:
            base_points: Базовые очки за фишку
            cascade_multiplier: Множитель за каскад
        """
        self._base_points = base_points
        self._cascade_multiplier = cascade_multiplier
    
    def score_for_removed(self, removed_count: int, cascade_index: int) -> int:
        """Рассчитать очки за удалённые фишки.
        
        Args:
            removed_count: Количество удалённых фишек
            cascade_index: Индекс каскада (≥0)
            
        Returns:
            int: Количество очков
            
        Raises:
            ValueError: Если параметры невалидны
        """
        if removed_count < 0:
            raise ValueError("Количество удалённых фишек не может быть отрицательным")
        
        if cascade_index < 0:
            raise ValueError("Индекс каскада не может быть отрицательным")
        
        # Базовые очки за фишки
        base_score = removed_count * self._base_points
        
        # Применяем множитель каскада
        multiplier = self._calculate_cascade_multiplier(cascade_index)
        
        return int(base_score * multiplier)
    
    def add_points(self, state, points: int) -> None:
        """Добавить очки к счёту.
        
        Args:
            state: Состояние игры
            points: Очки для добавления (≥0)
        """
        if points < 0:
            raise ValueError("Очки не могут быть отрицательными")
        
        state.add_score(points)
    
    def _calculate_cascade_multiplier(self, cascade_index: int) -> float:
        """Рассчитать множитель каскада.
        
        Args:
            cascade_index: Индекс каскада
            
        Returns:
            float: Множитель для очков
        """
        if cascade_index == 0:
            return 1.0
        
        # Экспоненциальный рост множителя
        return self._cascade_multiplier ** cascade_index
