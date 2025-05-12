from __future__ import annotations
from abc import ABC, abstractmethod


class BaseClientRec(ABC):
    @property
    @abstractmethod
    def role(self) -> str:
        pass

    @property
    @abstractmethod
    def params(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> BaseClientRec:
        pass
