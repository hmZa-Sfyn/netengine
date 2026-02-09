"""Example extension: Banner grabber."""

from netengine.extensions.base import BaseExtension
from netengine.utils import Logger
from netengine.networking import TCPHandler
from typing import Dict


class BannerGrabberExtension(BaseExtension):
    """Grab service banners from open ports."""

    def __init__(self):
        """Initialize banner grabber."""
        super().__init__("BannerGrabber", "1.0.0")
        self.logger = Logger()

    def execute(self, host: str, ports: list) -> Dict:
        """Grab banners from multiple ports."""
        tcp = TCPHandler(self.logger)
        banners = {}

        self.logger.info(f"Grabbing banners from {host}...")

        for port in ports:
            try:
                sock = tcp.connect(host, port, timeout=2.0)
                try:
                    sock.settimeout(1.0)
                    banner = sock.recv(1024).decode().strip()
                    banners[port] = banner
                    self.logger.success(f"Port {port}: {banner[:50]}")
                except:
                    banners[port] = ""
                finally:
                    sock.close()
            except:
                banners[port] = None

        return banners
