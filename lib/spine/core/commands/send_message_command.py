from typing import Dict, Self

from .base_command import BaseCommand
from ..enum import CommandEnum


class SendMessageCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.SEND_MESSAGE

    def __init__(self, connection_id: int, msg_data: Dict[str, any]):
        super().__init__()
        self._connection_id = connection_id
        self._msg_data = msg_data

    @property
    def connection_id(self) -> int:
        return self._connection_id

    @property
    def msg_data(self) -> Dict[str, any]:
        return self._msg_data

    def to_dict(self):
        return {
            **super().to_dict(),
            'connection_id': self._connection_id,
            'msg_data': self._msg_data
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls(data['connection_id'], data['msg_data'])
