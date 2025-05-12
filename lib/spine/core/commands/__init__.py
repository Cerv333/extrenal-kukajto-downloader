from .base_command import BaseCommand
from .handshake_command import HandshakeCommand
from .handshake_response_command import HandshakeResponseCommand
from .ping_command import PingCommand
from .pong_command import PongCommand
from .error_command import ErrorCommand
from .register_service_command import RegisterServiceCommand
from .register_service_response_command import RegisterServiceResponseCommand
from .service_request_command import ServiceRequestCommand
from .connection_established_command import ConnectionEstablishedCommand
from .close_connection_command import CloseConnectionCommand
from .connection_closed_command import ConnectionClosedCommand
from .send_message_command import SendMessageCommand
from .message_received_command import MessageReceivedCommand


command_classes = [HandshakeCommand, PingCommand, PongCommand, ErrorCommand, HandshakeResponseCommand, RegisterServiceCommand, RegisterServiceResponseCommand,
                   ServiceRequestCommand, ConnectionEstablishedCommand, CloseConnectionCommand, ConnectionClosedCommand, SendMessageCommand,
                   MessageReceivedCommand]
