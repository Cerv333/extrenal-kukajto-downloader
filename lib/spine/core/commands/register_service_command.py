from __future__ import annotations
from typing import Dict, Self, Optional

from .base_command import BaseCommand
from ..error import SpineError
from ..enum import CommandEnum
from ..model import BaseServiceRec, service_rec_classes


class RegisterServiceCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.REGISTER_SERVICE

    def __init__(self, service_rec: BaseServiceRec, custom_id: Optional[int] = None):
        super().__init__()
        self._service_rec = service_rec
        self._custom_id = custom_id

    @property
    def service_rec(self) -> BaseServiceRec:
        return self._service_rec

    @property
    def custom_id(self) -> Optional[int]:
        return self._custom_id

    def to_dict(self):
        return {
            **super().to_dict(),
            'type': self._service_rec.service_type,
            'str_code': self._service_rec.str_code,
            'single': self._service_rec.single,
            'params': self._service_rec.params,
            'custom_id': self._custom_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        service_rec_class = service_rec_classes.get(data['type'])
        if service_rec_class is None:
            raise SpineError(f'Unknown service type: {data["type"]}')
        else:
            service_rec = service_rec_class.from_dict(data['str_code'], data['single'], data['params'])
            return cls(service_rec, custom_id=data.get('custom_id'))
