from __future__ import annotations

from queue import Queue, Empty
from threading import Thread
from typing import Optional, Callable

from websocket import WebSocket, WebSocketConnectionClosedException, WebSocketTimeoutException

from .command_loading import deserialize_command
from .commands import BaseCommand


class SpineSession:
    def __init__(self, websocket: WebSocket, on_close: Callable[[SpineSession], None]):
        self._websocket = websocket
        self._on_close = on_close
        self._queue = Queue()
        self._recv_thread = Thread(target=self._recv_loop, daemon=True)
        self._recv_thread.start()

    @property
    def connected(self) -> bool:
        return self._websocket is not None and self._websocket.connected

    def send(self, command: BaseCommand) -> None:
        try:
            self._websocket.send(command.serialize())
        except WebSocketConnectionClosedException as e:
            self.close()
            raise e

    def receive(self, timeout: Optional[float]) -> Optional[BaseCommand]:
        try:
            raw_data = self._queue.get(timeout=timeout)
            if raw_data is not None:
                return deserialize_command(raw_data) if raw_data else None
            else:
                self.close()
                raise WebSocketConnectionClosedException("Connection closed")
        except Empty:
            raise WebSocketTimeoutException("Timeout expired")

    def receive_waiting(self) -> Optional[BaseCommand]:
        while True:
            if not self._queue.empty():
                raw_data = self._queue.get()
                if raw_data is not None:
                    command = deserialize_command(raw_data) if raw_data else None
                    if command is not None:
                        return command
                else:
                    self.close()
                    raise WebSocketConnectionClosedException("Connection closed")
            else:
                return None

    def _recv_loop(self):
        try:
            while self.connected:
                try:
                    self._websocket.settimeout(15)
                    raw_data = self._websocket.recv()
                    if raw_data:
                        self._queue.put(raw_data)
                except WebSocketTimeoutException:
                    pass
        except WebSocketConnectionClosedException:
            pass
        finally:
            self._queue.put(None)

    def close(self) -> None:
        if self._websocket is not None:
            try:
                self._websocket.close()
            finally:
                self._websocket = None
                self._on_close(self)
