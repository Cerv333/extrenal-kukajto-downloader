from datetime import datetime
from typing import Callable, Optional, List, Dict, Tuple, Union

from websocket import WebSocketTimeoutException

from .base import BaseMessanger, BaseConsumer, ServiceProvider
from ..core import BaseClientRec, spine_client, HandshakeCommand, CommandEnum, SpineError, ServiceRequest, ServiceRequestCommand, BaseCommand,\
    ConnectionEstablishedCommand, ErrorCommand, ConnectionClosedCommand, PingCommand, PongCommand, SendMessageCommand, CloseConnectionCommand, BaseServiceRec,\
    RegisterServiceCommand, RegisterServiceResponseCommand, MessageReceivedCommand, SpineSession


class SpineMessanger(BaseMessanger):
    def __init__(self, access_token: str, client_rec: BaseClientRec):
        self._base_client_rec = client_rec
        self._access_token = access_token
        self._session: SpineSession = None
        self._client_id = None
        self._custom_id = 0
        self._commands: List[BaseCommand] = []
        self._consumers: Dict[int, BaseConsumer] = {}
        self._service_providers: Dict[int, ServiceProvider] = {}

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    @property
    def connected(self) -> bool:
        return self._session is not None and self._session.connected

    @property
    def client_id(self) -> Optional[int]:
        return self._client_id

    def start(self) -> int:
        if self._session is None:
            self._session = spine_client.open_session(self._access_token)
            try:
                self._session.send(HandshakeCommand(self._base_client_rec))
                response_command = self._session.receive(25)
                if response_command is not None:
                    if response_command.command_name == CommandEnum.HANDSHAKE_RESPONSE:
                        self._client_id = response_command.client_id
                        return self._client_id
                    elif response_command.command_name == CommandEnum.ERROR:
                        raise SpineError(response_command.error)
                    else:
                        raise SpineError(f"Unexpected response command: {response_command.command_name}")
            except Exception as e:
                self.stop()
                raise e
        else:
            raise SpineError("Spine messanger is already started. Please stop it before starting again.")

    def stop(self):
        self._check_session()
        for consumer in self._consumers.values():
            consumer.mark_closed()
        self._consumers.clear()
        self._session.close()
        self._session = None
        self._client_id = None

    def create_consumer(self, service_request: ServiceRequest, raise_error: bool = True) -> Optional[BaseConsumer]:
        self._check_session()
        custom_id = self._get_custom_id()
        self._session.send(ServiceRequestCommand(service_request, custom_id))
        command = self._next_command(lambda cmd: cmd.command_name in [CommandEnum.CONNECTION_ESTABLISHED, CommandEnum.ERROR] and cmd.custom_id == custom_id,
                                     wait=True, timeout=30, raise_for_none=True)
        if isinstance(command, ConnectionEstablishedCommand):
            consumer = BaseConsumer(self, command)
            self._consumers[consumer.connection_id] = consumer
            return consumer
        elif isinstance(command, ErrorCommand):
            if raise_error:
                raise SpineError(command.error)
            else:
                return None
        else:
            raise SpineError('Unexpected command received.')

    def create_service(self, service_rec: BaseServiceRec) -> ServiceProvider:
        self._check_session()
        custom_id = self._get_custom_id()
        self._session.send(RegisterServiceCommand(service_rec, custom_id))
        command = self._next_command(lambda cmd: cmd.command_name in [CommandEnum.REGISTER_SERVICE_RESPONSE, CommandEnum.ERROR] and cmd.custom_id == custom_id,
                                     wait=True, timeout=30, raise_for_none=True)
        if isinstance(command, RegisterServiceResponseCommand):
            service_provider = ServiceProvider(self, command)
            self._service_providers[service_provider.service_id] = service_provider
            return service_provider
        elif isinstance(command, ErrorCommand):
            raise SpineError(command.error)
        else:
            raise SpineError('Unexpected command received.')

    def send_message(self, consumer: BaseConsumer, msg_data: dict) -> None:
        self._check_session()
        if consumer.connection_id not in self._consumers:
            raise SpineError('Consumer is not registered.')
        else:
            self._session.send(SendMessageCommand(consumer.connection_id, msg_data))

    def receive_message(self, consumer: BaseConsumer, timeout: int = 30) -> dict:
        self._check_session()
        if consumer.connection_id not in self._consumers:
            raise SpineError("Consumer is not registered.")
        else:
            command: Optional[MessageReceivedCommand] = self._next_command(
                lambda cmd: cmd.command_name == CommandEnum.MESSAGE_RECEIVED and cmd.connection_id == consumer.connection_id, wait=True, timeout=timeout,
                raise_for_none=True, for_consumer=consumer)
            if command is None:
                raise SpineError("No message received.")
            else:
                return command.msg_data

    def wait_for_new_consumer(self, service_provider: ServiceProvider, timeout: Optional[int] = None) -> Optional[BaseConsumer]:
        self._check_session()
        if service_provider.service_id not in self._service_providers:
            raise SpineError("Service provider is not registered.")
        else:
            command: Optional[ConnectionEstablishedCommand] = self._next_command(
                lambda cmd: cmd.command_name == CommandEnum.CONNECTION_ESTABLISHED and cmd.service_id == service_provider.service_id,
                wait=True, timeout=timeout, raise_for_none=False)
            if command is None:
                return None
            else:
                consumer = BaseConsumer(self, command)
                self._consumers[consumer.connection_id] = consumer
                return consumer

    def wait_for_consumer_action(self, consumers: Optional[List[BaseConsumer]] = None, timeout: Optional[int] = None) -> Tuple[Optional[BaseConsumer], bool]:
        self._check_session()
        cmd_names = [CommandEnum.CONNECTION_ESTABLISHED, CommandEnum.CONNECTION_CLOSED, CommandEnum.MESSAGE_RECEIVED]
        if consumers is None:
            connection_ids = [c.connection_id for c in list(self._consumers.values())]

            def filter_fn(cmd):
                return cmd.command_name in cmd_names and cmd.connection_id in connection_ids
        else:
            def filter_fn(cmd):
                return cmd.command_name in cmd_names

        command: Optional[Union[ConnectionEstablishedCommand, ConnectionClosedCommand, MessageReceivedCommand]] = self._next_command(
            filter_fn, wait=True, timeout=timeout, raise_for_none=True, peek=True)
        if command is None:
            return None, False
        else:
            consumer = self._consumers.get(command.connection_id)
            readable = command.command_name == CommandEnum.MESSAGE_RECEIVED
            return consumer, readable

    def close_consumer(self, consumer: BaseConsumer) -> None:
        self._check_session()
        if consumer.connection_id not in self._consumers:
            raise SpineError("Consumer is not registered.")
        else:
            self._session.send(CloseConnectionCommand(consumer.connection_id))
            consumer.mark_closed()

    def load_waiting_commands(self) -> None:
        self._check_session()
        while True:
            command = self._session.receive_waiting()
            if command is not None:
                if not self._internal_process(command):
                    self._commands.append(command)
            else:
                break

    def _get_custom_id(self) -> int:
        self._custom_id = self._custom_id + 1
        return self._custom_id

    def _check_session(self) -> None:
        if self._session is None:
            raise SpineError("Spine messanger is not started. Please start it before using.")
        elif not self._session.connected:
            raise SpineError("Spine messanger is not connected.")

    def _next_command(self, filter_fn: Callable[[BaseCommand], bool], wait: bool = True, timeout: int = 30, raise_for_none: bool = False,
                      for_consumer: Optional[BaseConsumer] = None, peek: bool = False) -> Optional[BaseCommand]:
        for i, command in enumerate(self._commands):
            if filter_fn(command):
                return self._commands.pop(i)
        if wait:
            start = datetime.now()
            command = None
            while True:
                if for_consumer is not None and for_consumer.closed:
                    raise SpineError("Consumer is closed.")
                else:
                    now = datetime.now()
                    cur_timeout = timeout - (now - start).total_seconds() if timeout is not None else None
                    if cur_timeout is not None and cur_timeout <= 0:
                        if raise_for_none:
                            raise SpineError("Timeout expired")
                        else:
                            return None
                    else:
                        try:
                            command = self._session.receive(cur_timeout)
                        except WebSocketTimeoutException as e:
                            if raise_for_none:
                                raise SpineError("Timeout expired") from e
                            else:
                                return None
                        processed = self._internal_process(command)
                        if command is not None:
                            if filter_fn(command):
                                if not processed and peek:
                                    self._commands.append(command)
                                return command
                            else:
                                if not processed:
                                    self._commands.append(command)
                                command = None
        else:
            return None

    def _internal_process(self, command: Optional[BaseCommand]) -> bool:
        if command is None:
            return False
        else:
            command_name = command.command_name
            if command_name == ConnectionClosedCommand.COMMAND_NAME:
                consumer = self._consumers.get(command.connection_id)
                if consumer is not None:
                    consumer.mark_closed()
                    del self._consumers[command.connection_id]
                return True
            elif command_name == PingCommand.COMMAND_NAME:
                self._session.send(PongCommand())
                return True
            else:
                return False

    def _has_command(self, filter_fn: Callable[[BaseCommand], bool]) -> bool:
        for command in self._commands:
            if filter_fn(command):
                return True
        return False
