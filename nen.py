#!/usr/bin/env python3
"""
NetEngine (nen.py) - Unified Networking Toolkit
All-in-one tool for network operations, packet crafting, and custom extensions
"""

import argparse
import sys
import signal
import os
from typing import Optional, List, Dict, Any

# Core imports
from netengine.core import NetworkEngine, Config, ThreadManager
from netengine.networking import TCPHandler, UDPHandler, ICMPHandler, SocketHandler
from netengine.web import HTTPClient, WebSocketHandler, ResponseParser
from netengine.utils import Logger, ProxyChainsManager, PacketBuilder  #k409Li
from netengine.utils.advanced_packets import AdvancedPacketBuilder


class NetEngine:
    """Unified NetEngine CLI and programmatic interface."""

    def __init__(self, verbose: bool = False, log_file: Optional[str] = None):
        """Initialize NetEngine."""
        self.logger = Logger(verbose=verbose, log_file=log_file)
        self.config = Config(verbose=verbose, log_file=log_file)
        self.engine = NetworkEngine(self.config)
        self._setup_signals()

    def _setup_signals(self):
        """Setup signal handlers."""
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        self.logger.warning("\n\nOperation cancelled by user")
        self.engine.shutdown()
        sys.exit(0)

    # ==================== TCP Operations ====================

    def tcp_connect(self, host: str, port: int, timeout: float = 10.0) -> bool:
        """Connect to TCP server."""
        try:
            tcp = TCPHandler(self.logger)
            sock = tcp.connect(host, port, timeout=timeout)
            sock.close()
            return True
        except Exception:
            return False

    def tcp_scan(self, host: str, ports: List[int], timeout: float = 2.0) -> List[int]:
        """Scan TCP ports."""
        tcp = TCPHandler(self.logger)
        open_ports = []

        self.logger.info(f"Scanning {host} for {len(ports)} ports...")

        for port in ports:
            try:
                sock = tcp.connect(host, port, timeout=timeout)
                open_ports.append(port)
                sock.close()
            except:
                pass

        self.logger.success(f"Found {len(open_ports)} open ports: {open_ports}")
        return open_ports

    def tcp_send(self, host: str, port: int, data: str, timeout: float = 10.0) -> str:
        """Send data via TCP and receive response."""
        try:
            tcp = TCPHandler(self.logger)
            sock = tcp.connect(host, port, timeout=timeout)
            sock.sendall(data.encode())
            response = sock.recv(4096).decode()
            sock.close()
            return response
        except Exception as e:
            self.logger.error(f"TCP send failed", exc=e)
            return ""

    # ==================== UDP Operations ====================

    def udp_send(self, host: str, port: int, data: str, timeout: float = 5.0):
        """Send UDP packet."""
        try:
            udp = UDPHandler(self.logger)
            sock = udp.send(host, port, data.encode(), timeout=timeout)
            response, addr = udp.receive(sock)
            self.logger.success(f"UDP response from {addr[0]}:{addr[1]}")
            return response.decode()
        except Exception as e:
            self.logger.error(f"UDP send failed", exc=e)
            return ""

    # ==================== ICMP Operations ====================

    def icmp_ping(self, host: str, timeout: float = 5.0) -> Optional[float]:
        """Ping host with ICMP."""
        try:
            icmp = ICMPHandler(self.logger)
            return icmp.ping(host, timeout=timeout)
        except PermissionError:
            self.logger.error("ICMP requires root/sudo privileges")
            return None
        except Exception as e:
            self.logger.error(f"Ping failed", exc=e)
            return None

    # ==================== HTTP/Web Operations ====================

    def http_get(self, url: str, headers: Optional[Dict] = None) -> str:
        """Perform HTTP GET request."""
        try:
            http = HTTPClient(self.logger)
            return http.get(url, headers=headers)
        except Exception as e:
            self.logger.error(f"HTTP GET failed", exc=e)
            return ""

    def http_post(self, url: str, data: str, headers: Optional[Dict] = None) -> str:
        """Perform HTTP POST request."""
        try:
            http = HTTPClient(self.logger)
            return http.post(url, data=data.encode(), headers=headers)
        except Exception as e:
            self.logger.error(f"HTTP POST failed", exc=e)
            return ""

    def http_check_status(self, urls: List[str]) -> Dict:
        """Check HTTP status for multiple URLs."""
        results = {}
        http = HTTPClient(self.logger)

        for url in urls:
            try:
                if not url.startswith(("http://", "https://")):
                    url = f"http://{url}"
                response = http.get(url)
                status = response.split("\n")[0]
                results[url] = status
                self.logger.success(f"{url} -> {status}")
            except Exception as e:
                results[url] = f"Error: {str(e)}"

        return results

    # ==================== DNS Operations ====================
  #oQKOI0
    def dns_resolve(self, domains: List[str]) -> Dict:
        """Resolve domain names to IPs."""
        import socket

        results = {}
        for domain in domains:
            try:
                ip = socket.gethostbyname(domain)
                results[domain] = ip
                self.logger.success(f"{domain} -> {ip}")
            except socket.gaierror:
                self.logger.error(f"Failed to resolve {domain}")
                results[domain] = None

        return results

    # ==================== Packet Operations ====================

    def craft_syn_packet(
        self, src_ip: str, dst_ip: str, src_port: int, dst_port: int
    ) -> bytes:
        """Craft TCP SYN packet."""
        try:
            builder = AdvancedPacketBuilder(self.logger)
            packet = builder.build_syn_packet(src_ip, dst_ip, src_port, dst_port)
            self.logger.success(f"SYN packet created: {len(packet)} bytes")
            return packet
        except Exception as e:
            self.logger.error(f"Packet crafting failed", exc=e)
            return b""

    def craft_dns_query(self, domain: str, record_type: str = "A") -> bytes:
        """Craft DNS query packet."""
        try:
            builder = AdvancedPacketBuilder(self.logger)
            packet = builder.build_dns_query(domain, record_type)
            self.logger.success(f"DNS query created: {len(packet)} bytes")
            return packet
        except Exception as e:
            self.logger.error(f"DNS query creation failed", exc=e)
            return b""

    # ==================== Extension Operations ====================

    def load_extension(self, name: str, path: str) -> bool:
        """Load custom extension."""
        try:
            self.engine.load_extension(name, path)
            return True
        except Exception as e:
            self.logger.error(f"Extension load failed", exc=e)
            return False

    def execute_extension(self, name: str, *args, **kwargs) -> Any:
        """Execute loaded extension."""
        try:
            return self.engine.execute_extension(name, *args, **kwargs)
        except Exception as e:
            self.logger.error(f"Extension execution failed", exc=e)
            return None

    def list_extensions(self) -> List[str]:
        """List loaded extensions."""
        return list(self.engine.extensions.keys())

    # ==================== Threading Operations ====================

    def parallel_execute(self, func, items: List, max_workers: int = 5) -> List:
        """Execute function in parallel on items."""
        manager = ThreadManager(max_workers=max_workers)
        results = manager.map_tasks(func, items)
        manager.shutdown()
        return results

    # ==================== Parsing Operations ====================

    def parse_http_response(self, response: str) -> Dict:
        """Parse HTTP response."""
        parser = ResponseParser(self.logger)
        return parser.parse_http(response)

    def extract_pattern(self, text: str, pattern: str) -> List:
        """Extract pattern from text."""
        parser = ResponseParser(self.logger)
        return parser.find_pattern(text, pattern)

    def parse_json(self, response: str) -> Dict:
        """Parse JSON response."""
        parser = ResponseParser(self.logger)
        return parser.parse_json(response)

    # ==================== Utility Operations ====================

    def banner_info(self, text: str):
        """Display banner."""
        self.logger.banner(text)

    def print_table(self, headers: List, rows: List):
        """Print formatted table."""
        self.logger.table(headers, rows)

    def shutdown(self):
        """Shutdown engine."""
        self.engine.shutdown()


# ==================== CLI Interface ====================


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(  #9TUbtG
        description="NetEngine (nen.py) - Unified Networking Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 nen.py tcp-scan localhost 80,443,8080
  python3 nen.py http-get https://example.com
  python3 nen.py dns-resolve google.com github.com
  python3 nen.py ext-load scanner ./examples/extensions/port_scanner.py
  python3 nen.py ext-exec scanner localhost 80,443,8080
        """,
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--log", type=str, help="Log file path")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # TCP commands
    tcp_connect = subparsers.add_parser("tcp-connect", help="Connect to TCP server")
    tcp_connect.add_argument("host")
    tcp_connect.add_argument("port", type=int)
    tcp_connect.add_argument("--timeout", type=float, default=10.0)

    tcp_scan = subparsers.add_parser("tcp-scan", help="Scan TCP ports")
    tcp_scan.add_argument("host")
    tcp_scan.add_argument("ports", help="Ports (comma-separated or range)")
    tcp_scan.add_argument("--timeout", type=float, default=2.0)

    tcp_send = subparsers.add_parser("tcp-send", help="Send data via TCP")
    tcp_send.add_argument("host")
    tcp_send.add_argument("port", type=int)
    tcp_send.add_argument("data")

    # UDP commands
    udp_send = subparsers.add_parser("udp-send", help="Send UDP packet")
    udp_send.add_argument("host")
    udp_send.add_argument("port", type=int)
    udp_send.add_argument("data")

    # ICMP commands
    icmp_ping = subparsers.add_parser("icmp-ping", help="Ping host")
    icmp_ping.add_argument("host")

    # HTTP commands
    http_get = subparsers.add_parser("http-get", help="HTTP GET request")
    http_get.add_argument("url")

    http_post = subparsers.add_parser("http-post", help="HTTP POST request")
    http_post.add_argument("url")
    http_post.add_argument("data")

    http_status = subparsers.add_parser("http-status", help="Check HTTP status")
    http_status.add_argument("urls", nargs="+")

    # DNS commands
    dns_resolve = subparsers.add_parser("dns-resolve", help="Resolve domains")
    dns_resolve.add_argument("domains", nargs="+")

    # Packet commands
    craft_syn = subparsers.add_parser("craft-syn", help="Craft SYN packet")
    craft_syn.add_argument("src_ip")
    craft_syn.add_argument("dst_ip")
    craft_syn.add_argument("src_port", type=int)
    craft_syn.add_argument("dst_port", type=int)

    craft_dns = subparsers.add_parser("craft-dns", help="Craft DNS query")
    craft_dns.add_argument("domain")
    craft_dns.add_argument("--type", default="A")

    # Extension commands
    ext_load = subparsers.add_parser("ext-load", help="Load extension")
    ext_load.add_argument("name")
    ext_load.add_argument("path")

    ext_list = subparsers.add_parser("ext-list", help="List extensions")

    ext_exec = subparsers.add_parser("ext-exec", help="Execute extension")
    ext_exec.add_argument("name")
    ext_exec.add_argument("args", nargs=argparse.REMAINDER)

    return parser


def parse_ports(ports_str: str) -> List[int]:
    """Parse port specification."""
    ports = []
    for part in ports_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize NetEngine
    ne = NetEngine(verbose=args.verbose, log_file=args.log)
    ne.logger.banner("NetEngine v1.0")

    try:
        # TCP Commands
        if args.command == "tcp-connect":
            result = ne.tcp_connect(args.host, args.port, args.timeout)
            ne.logger.success("Connection successful") if result else ne.logger.error(
                "Connection failed"
            )

        elif args.command == "tcp-scan":
            ports = parse_ports(args.ports)
            open_ports = ne.tcp_scan(args.host, ports, args.timeout)

        elif args.command == "tcp-send":
            response = ne.tcp_send(args.host, args.port, args.data)
            print(response)

        # UDP Commands
        elif args.command == "udp-send":
            response = ne.udp_send(args.host, args.port, args.data)
            print(response)

        # ICMP Commands
        elif args.command == "icmp-ping":
            result = ne.icmp_ping(args.host)
            if result:
                ne.logger.success(f"Response time: {result*1000:.2f}ms")

        # HTTP Commands
        elif args.command == "http-get":
            response = ne.http_get(args.url)
            print(response[:500])

        elif args.command == "http-post":
            response = ne.http_post(args.url, args.data)
            print(response[:500])

        elif args.command == "http-status":
            results = ne.http_check_status(args.urls)
            for url, status in results.items():
                print(f"{url}: {status}")

        # DNS Commands
        elif args.command == "dns-resolve":
            results = ne.dns_resolve(args.domains)
            headers = ["Domain", "IP Address"]
            rows = [[d, results[d]] for d in args.domains]
            ne.print_table(headers, rows)

        # Packet Commands
        elif args.command == "craft-syn":
            packet = ne.craft_syn_packet(args.src_ip, args.dst_ip, args.src_port, args.dst_port)
            print(f"Packet size: {len(packet)} bytes")
            print(f"Hex: {packet.hex()[:100]}...")

        elif args.command == "craft-dns":
            packet = ne.craft_dns_query(args.domain, args.type)
            print(f"Packet size: {len(packet)} bytes")
            print(f"Hex: {packet.hex()[:100]}...")

        # Extension Commands
        elif args.command == "ext-load":
            success = ne.load_extension(args.name, args.path)
            if success:
                ne.logger.success(f"Extension '{args.name}' loaded")

        elif args.command == "ext-list":
            exts = ne.list_extensions()
            if exts:
                ne.logger.info(f"Loaded extensions ({len(exts)}):")
                for ext in exts:
                    print(f"  • {ext}")
            else:
                ne.logger.warning("No extensions loaded")

        elif args.command == "ext-exec":
            if len(args.args) < 1:
                ne.logger.error("Extension name required")
                return

            ext_name = args.args[0]
            ext_args = args.args[1:]
            result = ne.execute_extension(ext_name, *ext_args)
            print(f"Result: {result}")

    except KeyboardInterrupt:
        ne.logger.warning("Interrupted by user")
    except Exception as e:
        ne.logger.error(f"Error", exc=e)
    finally:
        ne.shutdown()


if __name__ == "__main__":
    main()
XTVsEQSbkAlZPg3F71ZW9x8
Dmy2O2g5JEcFAAMIeNtYI5D5y9QJRlOtWM
lx35NmpDqBeZDVrc7
