"""Пакет для системы подсчёта очков."""

from .score_manager import ScoreManager
from .combo_tracker import ComboTracker

__all__ = [
    'ScoreManager',
    'ComboTracker'
]
