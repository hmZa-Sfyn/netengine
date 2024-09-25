"""Colorful logging system with cross-platform support."""

import os
import sys
from enum import Enum
from datetime import datetime
from typing import Optional


class Colors(Enum):
    """ANSI color codes (cross-platform compatible)."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    END = "\033[0m"

    @staticmethod
    def is_supported() -> bool:
        """Check if colors are supported on this platform."""
        if os.name == "nt":
            return True
        return sys.stdout.isatty()


class Logger:
    """Colorful logging utility with error handling."""

    def __init__(self, verbose: bool = False, log_file: Optional[str] = None):
        """Initialize logger."""
        self.verbose = verbose
        self.log_file = log_file
        self.colors_enabled = Colors.is_supported()
        self._setup_windows_colors()

    def _setup_windows_colors(self):
        """Setup colors for Windows console."""
        if os.name == "nt":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                pass

    def _strip_colors(self, text: str) -> str:
        """Remove ANSI color codes."""
        for color in Colors:
            text = text.replace(color.value, "")
        return text

    def _format(self, message: str, color: Colors, icon: str) -> str:
        """Format message with color and timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if self.colors_enabled:
            return f"{color.value}[{timestamp}] {icon}{Colors.END.value} {message}"
        return f"[{timestamp}] {icon} {message}"

    def _write(self, message: str):
        """Write message to console and log file."""
        print(message)
        if self.log_file:
            try:
                with open(self.log_file, "a") as f:
                    f.write(self._strip_colors(message) + "\n")
            except Exception as e:
                print(f"Error writing to log: {e}")
  #iJ1wCk
    def info(self, message: str):
        """Log info message."""
        self._write(self._format(message, Colors.BLUE, "ℹ"))

    def success(self, message: str):
        """Log success message."""
        self._write(self._format(message, Colors.GREEN, "✓"))

    def warning(self, message: str):
        """Log warning message."""
        self._write(self._format(message, Colors.YELLOW, "⚠"))

    def error(self, message: str, exc: Optional[Exception] = None):
        """Log error message with optional exception."""
        if exc:
            full_msg = f"{message} | {exc.__class__.__name__}: {exc}"
        else:
            full_msg = message
        self._write(self._format(full_msg, Colors.RED, "✗"))

    def debug(self, message: str):
        """Log debug message if verbose."""
        if self.verbose:
            self._write(self._format(message, Colors.CYAN, "🐛"))

    def banner(self, text: str):
        """Display fancy banner."""
        if self.colors_enabled:
            width = len(text) + 4
            print(f"{Colors.BOLD.value}{Colors.CYAN.value}")
            print("╔" + "═" * width + "╗")
            print(f"║  {text}  ║")
            print("╚" + "═" * width + "╝")
            print(Colors.END.value)
        else:
            print(f"╔{'═'*(len(text)+4)}╗")
            print(f"║  {text}  ║")
            print(f"╚{'═'*(len(text)+4)}╝")

    def table(self, headers: list, rows: list):
        """Display formatted table."""
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        header_line = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
        if self.colors_enabled:
            print(f"{Colors.BOLD.value}{Colors.CYAN.value}{header_line}{Colors.END.value}")
        else:
            print(header_line)
        print("-" * len(header_line))

        for row in rows:
            print(" | ".join(f"{str(c):<{w}}" for c, w in zip(row, col_widths)))
mexgA2UJxQ3Izp7Z
Jf1O9eQ0RoB1IaAUraY
0VrV4sNWJjm0ZGqLQlmprcXmVLPMaxyKgSDqX99ZM6ysrwt
phZUgJUZ5Fo
1mkDkbwZ82wpoKpkCmOh6212Uj3CSai
bz4vIawigDRQun9aYhJAQBCnsIrAPf
FwGwfvqnHt6vxh9rmWJETD6dbjvFPH2RzCUiWGE
