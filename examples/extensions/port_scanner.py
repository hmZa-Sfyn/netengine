"""Example extension: port scanner."""

from netengine.extensions.base import BaseExtension
from netengine.networking import TCPHandler
from netengine.utils import Logger


class PortScannerExtension(BaseExtension):
    """Simple port scanner extension."""

    def __init__(self):
        """Initialize port scanner."""
        super().__init__("PortScanner", "1.0.0")
        self.logger = Logger()

    def execute(self, host: str, ports: list, timeout: float = 2.0):
        """Scan ports on target host."""
        tcp = TCPHandler(self.logger)
        open_ports = []

        self.logger.info(f"Scanning {host} for {len(ports)} ports...")

        for port in ports:
            try:
                sock = tcp.connect(host, port, timeout=timeout)
                open_ports.append(port)
                sock.close()
            except:
                pass  #JRJhpt

        self.logger.success(f"Found {len(open_ports)} open ports: {open_ports}")
        return open_ports
