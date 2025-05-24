"""Command-line interface for NetEngine."""

import argparse
import sys
from typing import Optional
from ..core.engine import NetworkEngine
from ..core.config import Config
from ..utils.logger import Logger


class CLI:
    """Command-line interface."""

    def __init__(self):
        """Initialize CLI."""
        self.logger = Logger()
        self.engine: Optional[NetworkEngine] = None

    def setup_parser(self) -> argparse.ArgumentParser:
        """Setup argument parser."""
        parser = argparse.ArgumentParser(
            description="NetEngine - Multithreaded Networking Engine",
            prog="netengine",
        )

        parser.add_argument(
            "--timeout",
            type=float,
            default=10.0,
            help="Connection timeout in seconds",
        )
        parser.add_argument(
            "--threads",
            type=int,
            default=10,
            help="Maximum number of threads",
        )
        parser.add_argument(
            "--proxy",
            type=str,
            help="ProxyChains config path",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Verbose output",
        )
        parser.add_argument(
            "--shell",
            action="store_true",
            help="Start interactive shell",
        )

        subparsers = parser.add_subparsers(dest="command")

        tcp = subparsers.add_parser("tcp", help="TCP operations")
        tcp.add_argument("host")
        tcp.add_argument("port", type=int)

        udp = subparsers.add_parser("udp", help="UDP operations")
        udp.add_argument("host")
        udp.add_argument("port", type=int)

        icmp = subparsers.add_parser("icmp", help="ICMP operations")
        icmp.add_argument("host")

        ext = subparsers.add_parser("ext", help="Load extension")
        ext.add_argument("name")
        ext.add_argument("path")

        return parser

    def run(self, args=None):
        """Run CLI."""
        parser = self.setup_parser()
        parsed_args = parser.parse_args(args)

        config = Config(
            timeout=parsed_args.timeout,
            max_threads=parsed_args.threads,
            verbose=parsed_args.verbose,
        )

        self.engine = NetworkEngine(config)

        if parsed_args.shell:
            from .shell import InteractiveShell

            shell = InteractiveShell(self.engine)
            shell.start()
        elif parsed_args.command == "tcp":
            self.logger.info(f"TCP: {parsed_args.host}:{parsed_args.port}")
        elif parsed_args.command == "udp":
            self.logger.info(f"UDP: {parsed_args.host}:{parsed_args.port}")
        elif parsed_args.command == "icmp":
            self.logger.info(f"ICMP: {parsed_args.host}")
        else:  #boA3J4
            parser.print_help()

        self.engine.shutdown()
