from typing import Optional

from .service_request import ServiceRequest
from ...enum import ServiceTypeEnum


class WebBrowserServiceRequest(ServiceRequest):
    def __init__(self, machine: Optional[str], browser: Optional[str], system: Optional[str], blocking: bool):
        super().__init__(blocking)
        self._machine = machine
        self._browser = browser
        self._system = system

    @property
    def service_type(self) -> str:
        return ServiceTypeEnum.WEB_BROWSER

    @property
    def machine(self) -> Optional[str]:
        return self._machine

    @property
    def browser(self) -> Optional[str]:
        return self._browser

    @property
    def system(self) -> Optional[str]:
        return self._system

    @property
    def params(self) -> dict:
        return {
            'machine': self._machine,
            'browser': self._browser,
            'system': self._system
        }

    @classmethod
    def from_dict(cls, blocking: bool, data: dict) -> ServiceRequest:
        return cls(machine=data.get('machine'), browser=data.get('browser'), system=data.get('system'), blocking=blocking)
