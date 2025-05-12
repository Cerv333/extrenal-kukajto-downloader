from __future__ import annotations

from typing import Dict, Self

from .base_command import BaseCommand
from ..enum import CommandEnum


class HandshakeResponseCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.HANDSHAKE_RESPONSE

    def __init__(self, client_id: int):
        super().__init__()
        self._client_id = client_id

    @property
    def client_id(self) -> int:
        return self._client_id

    def to_dict(self):
        return {
            **super().to_dict(),
            'client_id': self._client_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls(client_id=data['client_id'])
