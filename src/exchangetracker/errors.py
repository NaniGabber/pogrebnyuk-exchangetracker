class ExchangeTrackerError(Exception):
    """Базовий виняток застосунку."""

    pass


class SourceError(ExchangeTrackerError):
    """Проблема з джерелом даних: файл, мережа, формат."""

    pass


class ParseError(SourceError):
    """Запис не вдалося розібрати."""

    pass


class ConfigError(ExchangeTrackerError):
    """Некоректна конфігурація застосунку."""

    pass
