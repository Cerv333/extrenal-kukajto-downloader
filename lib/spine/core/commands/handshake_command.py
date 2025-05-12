from __future__ import annotations
from typing import Dict, Self

from .base_command import BaseCommand
from ..error import SpineError
from ..enum import CommandEnum
from ..model import BaseClientRec, client_rec_classes


class HandshakeCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.HANDSHAKE

    def __init__(self, client_rec: BaseClientRec):
        super().__init__()
        self._client_rec = client_rec

    @property
    def client_rec(self) -> BaseClientRec:
        return self._client_rec

    def to_dict(self):
        return {
            **super().to_dict(),
            'role': self._client_rec.role,
            'params': self._client_rec.params
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        client_rec_class = client_rec_classes.get(data['role'])
        if client_rec_class is None:
            raise SpineError(f'Unknown client role: {data["role"]}')
        else:
            client_rec = client_rec_class.from_dict(data.get('params'))
            return cls(client_rec)
