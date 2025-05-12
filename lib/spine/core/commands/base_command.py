from __future__ import annotations
from json import dumps, loads
from typing import Dict, Self


class BaseCommand:
    COMMAND_NAME = 'base_command'

    def __init__(self):
        pass

    @property
    def command_name(self):
        return self.__class__.COMMAND_NAME

    def to_dict(self):
        return {
            'command': self.command_name
        }

    def serialize(self):
        return dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Self:
        return cls()

    @classmethod
    def deserialize(cls, data: str) -> Self:
        return cls.from_dict(loads(data))

    @classmethod
    def is_suitable(cls, data: Dict[str, any]) -> bool:
        return data.get('command') == cls.COMMAND_NAME

    def __repr__(self):
        return f'{self.__class__.__name__}({self.to_dict()})'
