"""Interactive shell for NetEngine."""

import cmd
import sys
import signal
from typing import Optional
from ..core.engine import NetworkEngine
from ..utils.logger import Logger
from ..networking import TCPHandler, UDPHandler, ICMPHandler
from ..web import HTTPClient


class InteractiveShell(cmd.Cmd):
    """Interactive shell interface."""

    intro = """
╔════════════════════════════════════════════╗
║     NetEngine Interactive Shell v1.0       ║
║  Multithreaded Network Engine & Toolkit    ║
╚════════════════════════════════════════════╝

Type 'help' for available commands or 'help <command>'
Press Ctrl+C to interrupt current operation
"""

    prompt = "netengine> "

    def __init__(self, engine: NetworkEngine):
        """Initialize interactive shell."""
        super().__init__()
        self.engine = engine
        self.logger = Logger()
        self.tcp = TCPHandler(self.logger)
        self.udp = UDPHandler(self.logger)
        self.icmp = ICMPHandler(self.logger)
        self.http = HTTPClient(self.logger)
        self._setup_signals()

    def _setup_signals(self):
        """Setup signal handlers for graceful interrupt."""
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        self.logger.warning("\nOperation cancelled by user")
        raise KeyboardInterrupt()

    def do_tcp(self, args):
        """TCP <host> <port>: Connect to TCP server."""
        try:
            parts = args.split()
            if len(parts) != 2:
                self.logger.error("Usage: tcp <host> <port>")
                return
            host, port = parts[0], int(parts[1])
            sock = self.tcp.connect(host, port)
            self.logger.success(f"Connected successfully to {host}:{port}")
            sock.close()
        except KeyboardInterrupt:
            self.logger.warning("Cancelled by user")
        except ValueError:
            self.logger.error("Port must be a number")
        except Exception as e:
            self.logger.error(f"TCP operation failed", exc=e)

    def do_udp(self, args):
        """UDP <host> <port>: Send UDP packet."""
        try:
            parts = args.split()
            if len(parts) != 2:
                self.logger.error("Usage: udp <host> <port>")
                return
            host, port = parts[0], int(parts[1])
            sock = self.udp.send(host, port, b"NetEngine UDP Probe")
            self.logger.success(f"UDP packet sent to {host}:{port}")
            sock.close()
        except KeyboardInterrupt:
            self.logger.warning("Cancelled by user")
        except ValueError:
            self.logger.error("Port must be a number")
        except Exception as e:
            self.logger.error(f"UDP operation failed", exc=e)

    def do_icmp(self, args):
        """ICMP <host>: Ping host (requires sudo/admin)."""
        try:
            if not args:
                self.logger.error("Usage: icmp <host>")
                return
            self.icmp.ping(args.strip())
        except KeyboardInterrupt:
            self.logger.warning("Cancelled by user")
        except PermissionError:
            self.logger.error("ICMP requires elevated privileges (sudo/admin)")
        except Exception as e:
            self.logger.error(f"ICMP operation failed", exc=e)

    def do_http(self, args):
        """HTTP <url>: Perform HTTP GET request."""
        try:
            if not args:
                self.logger.error("Usage: http <url>")
                return
            response = self.http.get(args.strip())
            print(response[:500])
            self.logger.success(f"Retrieved {len(response)} bytes")
        except KeyboardInterrupt:
            self.logger.warning("Cancelled by user")
        except Exception as e:
            self.logger.error(f"HTTP request failed", exc=e)

    def do_ext(self, args):
        """EXT <name> <path>: Load extension."""
        try:
            parts = args.split()
            if len(parts) != 2:
                self.logger.error("Usage: ext <name> <path>")
                return
            self.engine.load_extension(parts[0], parts[1])
        except KeyboardInterrupt:
            self.logger.warning("Cancelled by user")
        except Exception as e:
            self.logger.error(f"Extension load failed", exc=e)

    def do_list(self, args):
        """LIST: List loaded extensions."""
        exts = self.engine.extensions.keys()
        if exts:
            self.logger.info(f"Loaded extensions ({len(exts)}):")
            for ext in exts:
                print(f"  • {ext}")
        else:
            self.logger.warning("No extensions loaded")

    def do_clear(self, args):
        """CLEAR: Clear screen."""
        import os
        os.system("cls" if os.name == "nt" else "clear")

    def do_exit(self, args):
        """EXIT: Exit shell."""
        self.logger.success("Goodbye!")
        return True

    def do_EOF(self, args):
        """Handle EOF."""
        return self.do_exit(args)

    def emptyline(self):
        """Handle empty input."""
        pass

    def default(self, line):
        """Handle unknown commands."""
        self.logger.warning(f"Unknown command: {line}")
        self.logger.info("Type 'help' for available commands")
