from json import loads
from typing import Dict, Type, Optional

from lib.error import WorkerError
from .commands import BaseCommand, command_classes


def find_command_cls(data: Dict[str, any]) -> Optional[Type[BaseCommand]]:
    for command_class in command_classes:
        if command_class.is_suitable(data):
            return command_class
    return None


def load_command(data: Dict[str, any], required: bool = True) -> Optional[BaseCommand]:
    command_class = find_command_cls(data)
    if command_class is None:
        if required:
            raise WorkerError(f'Command not found: {data}')
        else:
            return None
    else:
        return command_class.from_dict(data)


def deserialize_command(data: str, required: bool = True) -> Optional[BaseCommand]:
    return load_command(loads(data), required=required)
