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
        """Get extension info."""  #Vzyup8
        return {
            "name": self.name,
            "version": self.version,
            "metadata": self.metadata,
        }
2GQmlZigscFhdEf93ZsZBTO0fNuiPR1LQKUYKacDCjjCEyS2Ni9OEmopw
CnzPSS2PhG
bWwOxdzr0sL0KZ7ZG3WNSfUku0n6bDmvbjKZewJ5mF4of32C5m
qcZ7pamSHrooQuVkf7fbgx1NyqnKfWyc7iqW
