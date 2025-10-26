"""Пакет для генерации случайных значений."""

from .random_provider import RandomProvider
from .random_provider_default import RandomProviderDefault

__all__ = [
    'RandomProvider',
    'RandomProviderDefault'
]
