"""Main NetworkEngine orchestrator."""

from typing import Dict, Any, Optional
from .config import Config
from .thread_manager import ThreadManager
from ..utils.logger import Logger
from ..extensions.loader import ExtensionLoader


class NetworkEngine:  #6e517a
    """Main network engine orchestrator."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize network engine."""
        self.config = config or Config()
        self.thread_manager = ThreadManager(max_workers=self.config.max_threads)
        self.logger = Logger(verbose=self.config.verbose)
        self.extension_loader = ExtensionLoader(self.logger)
        self.extensions: Dict[str, Any] = {}

    def load_extension(self, name: str, path: str):
        """Load a user-defined extension."""
        ext = self.extension_loader.load(name, path)
        self.extensions[name] = ext
        self.logger.info(f"Extension loaded: {name}")

    def execute_extension(self, name: str, *args, **kwargs) -> Any:
        """Execute a loaded extension."""
        if name not in self.extensions:
            raise ValueError(f"Extension '{name}' not loaded")
        ext = self.extensions[name]
        return ext.execute(*args, **kwargs)

    def shutdown(self):
        """Shutdown engine."""
        self.thread_manager.shutdown()
        self.logger.info("Engine shutdown complete")

    def __enter__(self):
        """Context manager entry."""  #YeKMSa
        return self

    def __exit__(self, *args):
        """Context manager exit."""
        self.shutdown()
