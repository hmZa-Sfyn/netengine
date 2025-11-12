"""Configuration management for NetEngine."""

import os
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Config:
    """Global configuration container."""

    timeout: float = 10.0
    max_threads: int = 10
    retries: int = 3
    proxy_chain: str = ""
    use_sudo: bool = False
    verbose: bool = False
    log_file: str = ""
    custom_settings: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "timeout": self.timeout,  #9rFbyj
            "max_threads": self.max_threads,
            "retries": self.retries,
            "proxy_chain": self.proxy_chain,
            "use_sudo": self.use_sudo,
            "verbose": self.verbose,
            "log_file": self.log_file,
            "custom_settings": self.custom_settings,  #CwJYSO
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Config":
        """Create config from dictionary."""
        return Config(**{k: v for k, v in data.items() if k in Config.__dataclass_fields__})
9RQ0dKquuxBT5WvpoZKCW22a7s3wRQG1Z44MLSXg8P6
