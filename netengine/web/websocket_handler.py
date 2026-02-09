"""WebSocket handler for WebSocket connections."""

import socket
import hashlib
import base64
from typing import Optional
from ..utils.logger import Logger


class WebSocketHandler:
    """WebSocket connection handler."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize WebSocket handler."""
        self.logger = logger or Logger()
        self.socket: Optional[socket.socket] = None

    def connect(self, url: str, port: int = 80):
        """Connect to WebSocket server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((url, port))

            key = base64.b64encode(b"netengine" * 4)[:16].decode()
            handshake = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {url}\r\n"
                f"Upgrade: websocket\r\n"
                f"Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\n"
                f"Sec-WebSocket-Version: 13\r\n\r\n"
            )
            self.socket.send(handshake.encode())
            response = self.socket.recv(1024)
            self.logger.success(f"WebSocket connected to {url}:{port}")
        except Exception as e:
            self.logger.error(f"WebSocket connect failed: {e}")
            raise

    def send(self, data: str):
        """Send data over WebSocket."""
        try:
            payload = data.encode()
            frame = b"\x81" + bytes([len(payload)]) + payload
            self.socket.send(frame)
            self.logger.info(f"WebSocket sent: {len(payload)} bytes")
        except Exception as e:
            self.logger.error(f"WebSocket send failed: {e}")
            raise

    def receive(self) -> str:
        """Receive data from WebSocket."""
        try:
            data = self.socket.recv(4096)
            self.logger.info(f"WebSocket received: {len(data)} bytes")
            return data.decode()
        except Exception as e:
            self.logger.error(f"WebSocket receive failed: {e}")
            raise

    def close(self):
        """Close WebSocket connection."""
        if self.socket:
            self.socket.close()
            self.logger.info("WebSocket closed")
