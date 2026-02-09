"""ICMP protocol handler (ping, etc)."""

import socket
import struct
import time
from typing import Optional
from ..utils.logger import Logger


class ICMPHandler:
    """ICMP protocol handler."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize ICMP handler."""
        self.logger = logger or Logger()

    def ping(self, host: str, timeout: float = 5.0) -> Optional[float]:
        """Send ICMP echo request (ping)."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.settimeout(timeout)

            packet = self._create_icmp_packet()
            start = time.time()
            sock.sendto(packet, (host, 1))

            data = sock.recv(1024)
            elapsed = time.time() - start
            self.logger.success(f"ICMP ping {host}: {elapsed*1000:.2f}ms")
            return elapsed
        except PermissionError:
            self.logger.error("ICMP requires root/sudo privileges")
            raise
        except Exception as e:
            self.logger.error(f"ICMP ping failed: {e}")
            raise

    def _create_icmp_packet(self) -> bytes:
        """Create ICMP echo request packet."""
        icmp_type = 8
        code = 0
        checksum = 0
        packet_id = 1
        sequence = 1
        data = b"pingpong"

        header = struct.pack("!BBHHH", icmp_type, code, checksum, packet_id, sequence)
        checksum = self._checksum(header + data)
        header = struct.pack("!BBHHH", icmp_type, code, checksum, packet_id, sequence)
        return header + data

    @staticmethod
    def _checksum(data: bytes) -> int:
        """Calculate ICMP checksum."""
        sum_val = 0
        count_to = (len(data) // 2) * 2
        for i in range(0, count_to, 2):
            w = (data[i] << 8) + data[i + 1]
            sum_val += w

        if count_to < len(data):
            sum_val += data[-1]

        sum_val = (sum_val >> 16) + (sum_val & 0xFFFF)
        sum_val += sum_val >> 16
        return ~sum_val & 0xFFFF
