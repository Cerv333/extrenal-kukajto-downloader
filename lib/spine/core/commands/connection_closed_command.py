from typing import Dict, Self

from .base_command import BaseCommand
from ..enum import CommandEnum


class ConnectionClosedCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.CONNECTION_CLOSED

    def __init__(self, connection_id: int, abruptly: bool):
        super().__init__()
        self._connection_id = connection_id
        self._abruptly= abruptly

    @property
    def connection_id(self) -> int:
        return self._connection_id

    @property
    def abruptly(self) -> bool:
        return self._abruptly

    def to_dict(self):
        return {
            **super().to_dict(),
            'connection_id': self._connection_id,
            'abruptly': self._abruptly
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls(data['connection_id'], data['abruptly'])
