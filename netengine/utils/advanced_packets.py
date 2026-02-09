"""Advanced packet crafting for various protocols."""

import socket
import struct
import platform
from typing import Optional, Dict, Any
from ..utils.logger import Logger


class AdvancedPacketBuilder:
    """Build advanced custom packets."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize packet builder."""
        self.logger = logger or Logger()

    def build_syn_packet(
        self,
        src_ip: str,
        dst_ip: str,
        src_port: int,
        dst_port: int,
        seq: int = 1000,
    ) -> bytes:
        """Build TCP SYN packet."""
        try:
            ttl = 64
            protocol = socket.IPPROTO_TCP

            src_packed = socket.inet_aton(src_ip)
            dst_packed = socket.inet_aton(dst_ip)

            ip_version = 4
            ip_header_length = 5
            ip_header = struct.pack(
                "!BBHHHBBH",
                (ip_version << 4) + ip_header_length,
                0,
                40,
                0,
                0,
                ttl,
                protocol,
                0,
            ) + src_packed + dst_packed

            tcp_flags = 0x02
            window = 5840
            tcp_header = struct.pack(
                "!HHLLBBHHH",
                src_port,
                dst_port,
                seq,
                0,
                (5 << 4) + 0,
                tcp_flags,
                window,
                0,
                0,
            )

            checksum = self._checksum(ip_header + tcp_header)
            ip_header_fixed = struct.pack(
                "!BBHHHBBH",
                (ip_version << 4) + ip_header_length,
                0,
                40,
                0,
                0,
                ttl,
                protocol,
                checksum,
            ) + src_packed + dst_packed

            self.logger.debug("SYN packet built successfully")
            return ip_header_fixed + tcp_header
        except Exception as e:
            self.logger.error("Failed to build SYN packet", exc=e)
            raise

    def build_fin_packet(
        self, src_ip: str, dst_ip: str, src_port: int, dst_port: int
    ) -> bytes:
        """Build TCP FIN packet."""
        try:
            ttl = 64
            protocol = socket.IPPROTO_TCP

            src_packed = socket.inet_aton(src_ip)
            dst_packed = socket.inet_aton(dst_ip)

            ip_version = 4
            ip_header_length = 5
            ip_header = struct.pack(
                "!BBHHHBBH", (ip_version << 4) + ip_header_length, 0, 40, 0, 0, ttl, protocol, 0
            ) + src_packed + dst_packed

            tcp_flags = 0x01
            window = 5840
            tcp_header = struct.pack(
                "!HHLLBBHHH", src_port, dst_port, 1000, 0, (5 << 4) + 0, tcp_flags, window, 0, 0
            )

            checksum = self._checksum(ip_header + tcp_header)
            ip_header_fixed = struct.pack(
                "!BBHHHBBH",
                (ip_version << 4) + ip_header_length,
                0,
                40,
                0,
                0,
                ttl,
                protocol,
                checksum,
            ) + src_packed + dst_packed

            self.logger.debug("FIN packet built successfully")
            return ip_header_fixed + tcp_header
        except Exception as e:
            self.logger.error("Failed to build FIN packet", exc=e)
            raise

    def build_rst_packet(
        self, src_ip: str, dst_ip: str, src_port: int, dst_port: int
    ) -> bytes:
        """Build TCP RST packet."""
        try:
            ttl = 64
            protocol = socket.IPPROTO_TCP

            src_packed = socket.inet_aton(src_ip)
            dst_packed = socket.inet_aton(dst_ip)

            ip_version = 4
            ip_header_length = 5
            ip_header = struct.pack(
                "!BBHHHBBH", (ip_version << 4) + ip_header_length, 0, 40, 0, 0, ttl, protocol, 0
            ) + src_packed + dst_packed

            tcp_flags = 0x04
            window = 5840
            tcp_header = struct.pack(
                "!HHLLBBHHH", src_port, dst_port, 1000, 0, (5 << 4) + 0, tcp_flags, window, 0, 0
            )

            checksum = self._checksum(ip_header + tcp_header)
            ip_header_fixed = struct.pack(
                "!BBHHHBBH",
                (ip_version << 4) + ip_header_length,
                0,
                40,
                0,
                0,
                ttl,
                protocol,
                checksum,
            ) + src_packed + dst_packed

            self.logger.debug("RST packet built successfully")
            return ip_header_fixed + tcp_header
        except Exception as e:
            self.logger.error("Failed to build RST packet", exc=e)
            raise

    def build_dns_query(self, domain: str, record_type: str = "A") -> bytes:
        """Build DNS query packet."""
        try:
            transaction_id = 0x1234
            flags = 0x0100
            questions = 1

            header = struct.pack(
                "!HHHHHH", transaction_id, flags, questions, 0, 0, 0
            )

            qname = b""
            for label in domain.split("."):
                qname += struct.pack("!B", len(label)) + label.encode()
            qname += b"\x00"

            type_map = {"A": 1, "MX": 15, "NS": 2, "TXT": 16, "CNAME": 5}
            qtype = type_map.get(record_type, 1)
            question = struct.pack("!HH", qtype, 1)

            self.logger.debug(f"DNS query packet built for {domain}")
            return header + qname + question
        except Exception as e:
            self.logger.error("Failed to build DNS query", exc=e)
            raise

    @staticmethod
    def _checksum(data: bytes) -> int:
        """Calculate IP/TCP checksum."""
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
