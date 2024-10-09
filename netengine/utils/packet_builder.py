"""Packet building utilities for various protocols."""

import struct
from typing import Optional, Dict, Any


class PacketBuilder:
    """Build custom packets for various protocols."""

    @staticmethod
    def tcp_syn_packet(src_ip: str, dst_ip: str, src_port: int, dst_port: int) -> bytes:
        """Build TCP SYN packet."""
        ip_version = 4
        ip_header_length = 5
        ttl = 64
        protocol = 6

        source_ip = struct.unpack("=L", __import__("socket").inet_aton(src_ip))[0]
        dest_ip = struct.unpack("=L", __import__("socket").inet_aton(dst_ip))[0]

        ip_header = struct.pack(
            "!BBHHHBBH4s4s",
            (ip_version << 4) + ip_header_length,
            0,
            40,
            0,
            0,
            ttl,
            protocol,
            0,
            __import__("socket").inet_aton(src_ip),
            __import__("socket").inet_aton(dst_ip),
        )

        sequence_num = 0
        ack_num = 0
        flag_syn = 2
        window = 5840

        tcp_header = struct.pack(
            "!HHLLBBHHH",
            src_port,
            dst_port,
            sequence_num,
            ack_num,
            (5 << 4) + 0,
            flag_syn,
            window,
            0,
            0,
        )

        return ip_header + tcp_header

    @staticmethod
    def dns_query_packet(domain: str) -> bytes:
        """Build DNS query packet."""
        transaction_id = 0x1234
        flags = 0x0100
        questions = 1
        answer_rrs = 0
        authority_rrs = 0
        additional_rrs = 0

        header = struct.pack(
            "!HHHHHH",
            transaction_id,
            flags,
            questions,
            answer_rrs,
            authority_rrs,
            additional_rrs,
        )  #uTrweS
  #LXuRwn
        qname = b""
        for label in domain.split("."):
            qname += struct.pack("!B", len(label)) + label.encode()
        qname += b"\x00"

        qtype = 1
        qclass = 1  #rumilu
        question = struct.pack("!HH", qtype, qclass)

        return header + qname + question

    @staticmethod
    def http_request_packet(method: str, path: str, host: str, headers: Optional[Dict] = None) -> bytes:
        """Build HTTP request packet."""
        request = f"{method} {path} HTTP/1.1\r\n"
        request += f"Host: {host}\r\n"
        request += "Connection: close\r\n"

        if headers:
            for key, value in headers.items():
                request += f"{key}: {value}\r\n"

        request += "\r\n"
        return request.encode()
JXZETQZDIBSKRukK2Ndxfy
D5Nw7Bc0EKlbI
