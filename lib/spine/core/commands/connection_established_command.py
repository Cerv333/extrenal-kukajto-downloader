from __future__ import annotations

from typing import Dict, Self, Optional

from .base_command import BaseCommand
from ..enum import CommandEnum


class ConnectionEstablishedCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.CONNECTION_ESTABLISHED

    def __init__(self, connection_id: int, service_id: int = None, service_str_code: str = None, client_id: int = None, custom_id: Optional[int] = None):
        super().__init__()
        self._connection_id = connection_id
        self._service_id = service_id
        self._service_str_code = service_str_code
        self._client_id = client_id
        self._custom_id = custom_id

    @property
    def connection_id(self) -> int:
        return self._connection_id

    @property
    def service_id(self) -> int:
        return self._service_id

    @property
    def service_str_code(self) -> str:
        return self._service_str_code

    @property
    def client_id(self) -> int:
        return self._client_id

    @property
    def custom_id(self) -> Optional[int]:
        return self._custom_id

    def to_dict(self):
        return {
            **super().to_dict(),
            'connection_id': self._connection_id,
            'service_id': self._service_id,
            'service_str_code': self._service_str_code,
            'client_id': self._client_id,
            'custom_id': self._custom_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls(connection_id=data['connection_id'], service_id=data.get('service_id'), service_str_code=data.get('service_str_code'),
                   client_id=data.get('client_id'), custom_id=data.get('custom_id'))
