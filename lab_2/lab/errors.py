"""
Модуль для собственных исключений приложения.
"""

class AppError(Exception):
    """Базовый класс для всех исключений уровня приложения."""
    pass

class ValidationError(AppError):
    """Исключение, возникающее при некорректных данных (например, оценка < 0)."""
    pass

class DataSourceError(AppError):
    """Исключение при работе с источниками данных (файлы, CSV)."""
    pass

class StudentNotFoundError(AppError):
    """Исключение, возникающее, если студент с указанным ID не найден."""
    pass