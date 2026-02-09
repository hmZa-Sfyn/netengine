"""Proxychains integration and management."""

import subprocess
import os
from typing import Optional, List
from .logger import Logger


class ProxyChainsManager:
    """Manage proxychains configuration and execution."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize proxychains manager."""
        self.logger = logger or Logger()
        self.config_file = os.path.expanduser("~/.proxychains/proxychains.conf")
        self.enabled = False

    def set_config(self, config_path: str):
        """Set proxychains configuration file."""
        if os.path.exists(config_path):
            self.config_file = config_path
            self.logger.success(f"ProxyChains config set: {config_path}")
        else:
            self.logger.error(f"Config file not found: {config_path}")

    def enable(self):
        """Enable proxychains."""
        self.enabled = True
        self.logger.info("ProxyChains enabled")

    def disable(self):
        """Disable proxychains."""
        self.enabled = False
        self.logger.info("ProxyChains disabled")

    def run_with_proxychains(self, command: List[str]) -> str:
        """Execute command through proxychains."""
        if not self.enabled:
            self.logger.warning("ProxyChains not enabled")
            return ""

        try:
            proxychains_cmd = ["proxychains4", "-f", self.config_file] + command
            result = subprocess.run(proxychains_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.success(f"ProxyChains command executed")
            else:
                self.logger.error(f"ProxyChains error: {result.stderr}")
            return result.stdout
        except Exception as e:
            self.logger.error(f"ProxyChains failed: {e}")
            raise
