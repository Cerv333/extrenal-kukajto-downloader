from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Self, Optional

from .base_command import BaseCommand
from ..enum import CommandEnum


class ErrorCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.ERROR

    def __init__(self, error: str, fatal: bool, custom_id: Optional[int] = None):
        super().__init__()
        self._error = error
        self._fatal = fatal
        self._custom_id = custom_id

    @property
    def error(self) -> str:
        return self._error

    @property
    def fatal(self) -> bool:
        return self._fatal

    @property
    def custom_id(self) -> Optional[int]:
        return self._custom_id

    def to_dict(self):
        return {
            **super().to_dict(),
            'error': self._error,
            'fatal': self._fatal,
            'custom_id': self._custom_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls(error=data['error'], fatal=data['fatal'], custom_id=data.get('custom_id'))
