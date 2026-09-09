# SPDX-FileCopyrightText: Copyright (c) 2025 Yegor Bugayenko
# SPDX-License-Identifier: MIT
"""Собственные исключения пакета gitted.

Каждое исключение несёт информацию о шаге (step), на котором произошла
ошибка, и сохраняет исходную причину (cause) через цепочку исключений.
Это позволяет быстро идентифицировать источник сбоя по логам.
"""


class GittedError(Exception):
    """Базовое исключение пакета gitted.

    Атрибуты:
        step: название шага, на котором произошла ошибка
            (например, 'auth', 'generate', 'analyze', 'parse').
        cause: исходное исключение, ставшее причиной сбоя (может быть None).
    """

    def __init__(self, message: str, step: str = 'unknown', cause: Exception | None = None):
        super().__init__(message)
        self.step = step
        self.cause = cause

    def __str__(self) -> str:
        base = f"[step={self.step}] {super().__str__()}"
        if self.cause is not None:
            base += f" (cause: {type(self.cause).__name__}: {self.cause})"
        return base


class ConfigError(GittedError):
    """Ошибка конфигурации: отсутствуют или некорректны переменные окружения."""


class AuthError(GittedError):
    """Ошибка аутентификации: не удалось получить токен доступа."""


class GenerationError(GittedError):
    """Ошибка генерации commit message."""


class AnalysisError(GittedError):
    """Ошибка анализа commit message."""


class ParseError(GittedError):
    """Ошибка разбора ответа модели (например, нечисловая оценка)."""
