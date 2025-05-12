from __future__ import annotations

from typing import Dict, Self, Optional

from .base_command import BaseCommand
from ..enum import CommandEnum


class RegisterServiceResponseCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.REGISTER_SERVICE_RESPONSE

    def __init__(self, service_id: int, custom_id: Optional[int]):
        super().__init__()
        self._service_id = service_id
        self._custom_id = custom_id

    @property
    def service_id(self) -> Optional[int]:
        return self._service_id

    @property
    def custom_id(self) -> Optional[int]:
        return self._custom_id

    def to_dict(self):
        return {
            **super().to_dict(),
            'service_id': self._service_id,
            'custom_id': self._custom_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls(service_id=data['service_id'], custom_id=data.get('custom_id'))
