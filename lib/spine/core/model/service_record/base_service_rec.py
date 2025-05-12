from __future__ import annotations
from abc import ABC, abstractmethod


class BaseServiceRec(ABC):
    def __init__(self, str_code: str, single: bool):
        self._str_code = str_code
        self._single = single

    @property
    def str_code(self) -> str:
        return self._str_code

    @property
    def single(self) -> bool:
        return self._single

    @property
    @abstractmethod
    def service_type(self) -> str:
        pass

    @property
    @abstractmethod
    def params(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, str_code: str, single: bool, data: dict) -> BaseServiceRec:
        pass
