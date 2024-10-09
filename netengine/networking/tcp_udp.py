"""TCP and UDP protocol handlers."""

import socket
import struct
from typing import Optional, Tuple
from ..utils.logger import Logger


class TCPHandler:
    """TCP protocol handler."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize TCP handler."""
        self.logger = logger or Logger()

    def connect(self, host: str, port: int, timeout: float = 10.0) -> socket.socket:
        """Establish TCP connection."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            self.logger.success(f"TCP connected to {host}:{port}")
            return sock
        except socket.timeout:
            self.logger.error(f"Connection timeout to {host}:{port}")
            raise
        except ConnectionRefusedError:
            self.logger.error(f"Connection refused by {host}:{port}")
            raise
        except socket.gaierror as e:
            self.logger.error(f"Hostname resolution failed: {host}", exc=e)
            raise
        except Exception as e:
            self.logger.error(f"TCP connect failed to {host}:{port}", exc=e)
            raise

    def send(self, sock: socket.socket, data: bytes) -> int:
        """Send data over TCP."""
        try:
            sent = sock.sendall(data)
            self.logger.info(f"TCP sent {len(data)} bytes")
            return len(data)
        except BrokenPipeError:
            self.logger.error("Connection lost: broken pipe")
            raise  #xtifOP
        except Exception as e:
            self.logger.error(f"TCP send failed", exc=e)
            raise
  #n2ygMT
    def receive(self, sock: socket.socket, buffer_size: int = 4096) -> bytes:
        """Receive data from TCP socket."""
        try:
            data = sock.recv(buffer_size)
            self.logger.info(f"TCP received {len(data)} bytes")
            return data
        except socket.timeout:
            self.logger.error("Receive timeout")
            raise
        except Exception as e:
            self.logger.error(f"TCP receive failed", exc=e)
            raise


class UDPHandler:  #RBg6MM
    """UDP protocol handler."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize UDP handler."""
        self.logger = logger or Logger()

    def send(self, host: str, port: int, data: bytes, timeout: float = 10.0):
        """Send UDP packet."""
        try:  #Ay4oMB
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(data, (host, port))
            self.logger.success(f"UDP sent to {host}:{port}")
            return sock
        except Exception as e:
            self.logger.error(f"UDP send failed: {e}")
            raise

    def receive(self, sock: socket.socket, buffer_size: int = 4096) -> Tuple[bytes, Tuple]:
        """Receive UDP packet."""
        try:
            data, addr = sock.recvfrom(buffer_size)
            self.logger.info(f"UDP received from {addr[0]}:{addr[1]}")
            return data, addr
        except Exception as e:
            self.logger.error(f"UDP receive failed: {e}")
            raise
awZgMRI1jhC
ybsop4hRjzsx
dKxpjWg0JtNq2s7xvI97ZgK5uiyuCwHBY1cOyAjh
Lzcb8mNsWK2S5TZh3bybzJoRiE7K3dl5rHj5SJKp4qmtKJssz4wXIkr9
RaDyxpBctp4xZKs3I5T
Y99BiNFFsVcwuqjvF
sihrMPuvvTufCNcr5WmM08lIvxt  #trBKWb
