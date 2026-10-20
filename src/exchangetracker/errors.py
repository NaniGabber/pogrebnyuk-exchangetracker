class JobRadarError(Exception):
    """Базовий виняток застосунку."""

    pass


class SourceError(JobRadarError):
    """Проблема з джерелом даних: файл, мережа, формат."""

    pass


class ParseError(SourceError):
    """Запис не вдалося розібрати."""

    pass


class ConfigError(JobRadarError):
    """Некоректна конфігурація застосунку."""

    pass
