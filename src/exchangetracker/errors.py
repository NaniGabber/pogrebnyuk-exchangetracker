class ExchangeTrackerError(Exception):
    """Базовий виняток застосунку."""


class SourceError(ExchangeTrackerError):
    """Проблема з джерелом даних: файл, мережа, формат."""


class ParseError(SourceError):
    """Запис не вдалося розібрати."""


class ConfigError(ExchangeTrackerError):
    """Некоректна конфігурація застосунку."""
