from __future__ import annotations
from typing import Dict, Self, Optional

from .base_command import BaseCommand
from ..error import SpineError
from ..enum import CommandEnum
from ..model import ServiceRequest, service_request_classes


class ServiceRequestCommand(BaseCommand):
    COMMAND_NAME = CommandEnum.SERVICE_REQUEST

    def __init__(self, service_request: ServiceRequest, custom_id: Optional[int] = None):
        super().__init__()
        self._service_request = service_request
        self._custom_id = custom_id

    @property
    def service_request(self) -> ServiceRequest:
        return self._service_request

    @property
    def custom_id(self) -> Optional[int]:
        return self._custom_id

    def to_dict(self):
        return {
            **super().to_dict(),
            'type': self._service_request.service_type,
            'blocking': self._service_request.blocking,
            'params': self._service_request.params,
            'custom_id': self._custom_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        service_request_class = service_request_classes.get(data['type'])
        if service_request_class is None:
            raise SpineError(f'Unknown service request type: {data["type"]}')
        else:
            service_request = service_request_class.from_dict(data['blocking'], data['params'])
            return cls(service_request, data.get('custom_id'))
