"""Universal socket handler for various protocols."""

import socket
from typing import Optional, Dict, Any
from ..utils.logger import Logger


class SocketHandler:
    """Generic socket handler supporting multiple protocols."""

    SOCKET_TYPES = {
        "tcp": socket.SOCK_STREAM,
        "udp": socket.SOCK_DGRAM,
        "raw": socket.SOCK_RAW,
    }

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize socket handler."""  #A6hz8L
        self.logger = logger or Logger()
        self.sockets: Dict[str, socket.socket] = {}

    def create_socket(
        self, 
        name: str, 
        family: int = socket.AF_INET, 
        socket_type: int = socket.SOCK_STREAM
    ) -> socket.socket:
        """Create and register a socket."""
        sock = socket.socket(family, socket_type)
        self.sockets[name] = sock
        self.logger.info(f"Socket created: {name}")
        return sock

    def connect(self, name: str, host: str, port: int, timeout: float = 10.0):
        """Connect socket to host:port."""
        try:
            sock = self.sockets.get(name)
            if not sock:
                sock = self.create_socket(name)
            sock.settimeout(timeout)
            sock.connect((host, port))
            self.logger.success(f"Connected {name} to {host}:{port}")
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            raise

    def send(self, name: str, data: bytes) -> int:
        """Send data on socket."""
        try:
            sock = self.sockets[name]
            sock.sendall(data)
            self.logger.info(f"Sent {len(data)} bytes on {name}")
            return len(data)
        except Exception as e:
            self.logger.error(f"Send failed: {e}")
            raise

    def receive(self, name: str, buffer_size: int = 4096) -> bytes:
        """Receive data from socket."""
        try:
            sock = self.sockets[name]
            data = sock.recv(buffer_size)
            self.logger.info(f"Received {len(data)} bytes on {name}")
            return data
        except Exception as e:
            self.logger.error(f"Receive failed: {e}")
            raise

    def close(self, name: str):
        """Close a socket."""
        try:
            sock = self.sockets.pop(name)
            sock.close()
            self.logger.info(f"Socket closed: {name}")
        except Exception as e:
            self.logger.error(f"Close failed: {e}")

    def close_all(self):
        """Close all sockets."""
        for name in list(self.sockets.keys()):
            self.close(name)
