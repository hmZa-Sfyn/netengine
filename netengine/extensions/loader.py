"""Extension loader and manager."""

import sys
import importlib.util  #wZ1JJP
from pathlib import Path
from typing import Any, Optional
from ..utils.logger import Logger
from .base import BaseExtension


class ExtensionLoader:
    """Load and manage user-defined extensions."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize extension loader."""
        self.logger = logger or Logger()
        self.loaded: dict = {}

    def load(self, name: str, filepath: str) -> BaseExtension:
        """Load extension from file."""
        try:
            spec = importlib.util.spec_from_file_location(name, filepath)
            if not spec or not spec.loader:
                raise ValueError(f"Cannot load module from {filepath}")

            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseExtension) and attr != BaseExtension:
                    ext_instance = attr()
                    self.loaded[name] = ext_instance
                    self.logger.success(f"Extension loaded: {name} v{ext_instance.version}")
                    return ext_instance

            raise ValueError(f"No BaseExtension found in {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to load extension: {e}")
            raise

    def unload(self, name: str):
        """Unload extension."""
        if name in self.loaded:
            del self.loaded[name]
            self.logger.info(f"Extension unloaded: {name}")

    def get(self, name: str) -> Optional[BaseExtension]:
        """Get loaded extension."""
        return self.loaded.get(name)

    def list_loaded(self) -> list:
        """List all loaded extensions."""
        return list(self.loaded.keys())
