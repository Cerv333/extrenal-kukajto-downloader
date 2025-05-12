from .base_service_rec import BaseServiceRec
from ...enum import ServiceTypeEnum


class WebBrowserServiceRec(BaseServiceRec):
    def __init__(self, str_code: str, single: bool, machine: str, browser: str, system: str):
        super().__init__(str_code, single)
        self._machine = machine
        self._browser = browser
        self._system = system

    @property
    def service_type(self) -> str:
        return ServiceTypeEnum.WEB_BROWSER

    @property
    def machine(self) -> str:
        return self._machine

    @property
    def browser(self) -> str:
        return self._browser

    @property
    def system(self) -> str:
        return self._system

    @property
    def params(self) -> dict:
        return {
            'machine': self._machine,
            'browser': self._browser,
            'system': self._system
        }

    @classmethod
    def from_dict(cls, str_code: str, single: bool, data: dict) -> BaseServiceRec:
        return cls(str_code, single, machine=data['machine'], browser=data['browser'], system=data['system'])
