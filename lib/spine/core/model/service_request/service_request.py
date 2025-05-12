from __future__ import annotations
from abc import ABC, abstractmethod


class ServiceRequest(ABC):
    def __init__(self, blocking: bool):
        self._blocking = blocking

    @property
    def blocking(self) -> bool:
        return self._blocking

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
    def from_dict(cls, blocking: bool, data: dict) -> ServiceRequest:
        pass

