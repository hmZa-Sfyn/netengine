"""Base class for user-defined extensions."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseExtension(ABC):
    """Base class for all NetEngine extensions."""

    def __init__(self, name: str, version: str = "1.0.0"):
        """Initialize extension."""
        self.name = name
        self.version = version
        self.metadata: Dict[str, Any] = {}

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute extension logic."""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get extension info."""
        return {
            "name": self.name,
            "version": self.version,
            "metadata": self.metadata,
        }
