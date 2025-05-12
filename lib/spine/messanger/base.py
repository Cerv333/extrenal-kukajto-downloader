from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Generator

from ..core import ConnectionEstablishedCommand, SpineError, RegisterServiceResponseCommand


class BaseMessanger(ABC):
    @abstractmethod
    def send_message(self, consumer: BaseConsumer, msg_data: dict) -> None:
        pass

    @abstractmethod
    def receive_message(self, consumer: BaseConsumer, timeout: int = 30) -> dict:
        pass

    @abstractmethod
    def close_consumer(self, consumer: BaseConsumer) -> None:
        pass

    @abstractmethod
    def wait_for_new_consumer(self, service_provider: ServiceProvider, timeout: Optional[int] = None) -> Optional[BaseConsumer]:
        pass

    @abstractmethod
    def load_waiting_commands(self) -> None:
        pass


class BaseConsumer:
    def __init__(self, messanger: BaseMessanger, command: ConnectionEstablishedCommand):
        self._connection_id = command.connection_id
        self._closed = False
        self._messanger = messanger

    @property
    def connection_id(self) -> int:
        return self._connection_id

    @property
    def closed(self) -> bool:
        return self._closed

    def mark_closed(self) -> None:
        self._closed = True

    def receive_message(self, timeout: int = 30) -> dict:
        self._check_closed()
        return self._messanger.receive_message(self, timeout)

    def send_message(self, msg_data: dict) -> None:
        self._messanger.load_waiting_commands()
        self._check_closed()
        self._messanger.send_message(self, msg_data)

    def close(self) -> None:
        if not self._closed:
            self._messanger.close_consumer(self)

    def _check_closed(self) -> None:
        if self._closed:
            raise SpineError("Consumer is closed.")


class ServiceProvider:
    def __init__(self, messanger: BaseMessanger, command: RegisterServiceResponseCommand):
        self._service_id = command.service_id
        self._messanger = messanger

    def __iter__(self) -> Generator[BaseConsumer, None, None]:
        while True:
            yield self.wait_for_consumer()

    @property
    def service_id(self) -> int:
        return self._service_id

    def wait_for_consumer(self, timeout: Optional[int] = None) -> BaseConsumer:
        return self._messanger.wait_for_new_consumer(self, timeout)


