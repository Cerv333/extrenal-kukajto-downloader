from typing import Dict, Self

from .base_command import BaseCommand
from ..enum import CommandEnum


class CloseConnectionCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.CLOSE_CONNECTION

    def __init__(self, connection_id: int):
        super().__init__()
        self._connection_id = connection_id

    @property
    def connection_id(self) -> int:
        return self._connection_id

    def to_dict(self):
        return {
            **super().to_dict(),
            'connection_id': self._connection_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls(data['connection_id'])
