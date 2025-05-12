from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Self, Optional

from .base_command import BaseCommand
from ..enum import CommandEnum


class PingCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.PING

    def __init__(self, dt: Optional[datetime] = None):
        super().__init__()
        self._dt = dt or datetime.now(tz=timezone.utc)

    def to_dict(self):
        return {
            **super().to_dict(),
            'timestamp': self._dt.timestamp(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls(dt=datetime.fromtimestamp(data['timestamp'], tz=timezone.utc))
