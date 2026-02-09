"""Thread pool and concurrency management."""

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Any, List
from ..utils.logger import Logger


class ThreadManager:
    """Manages multithreading operations."""

    def __init__(self, max_workers: int = 10):
        """Initialize thread manager."""
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.logger = Logger()

    def submit_task(self, func: Callable, *args, **kwargs) -> Any:
        """Submit a single task to the thread pool."""
        return self.executor.submit(func, *args, **kwargs)

    def map_tasks(self, func: Callable, items: List[Any]) -> List[Any]:
        """Map function over multiple items using threads."""
        futures = [self.submit_task(func, item) for item in items]
        results = []
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                self.logger.error(f"Thread error: {e}")
        return results

    def shutdown(self, wait: bool = True):
        """Shutdown thread pool."""
        self.executor.shutdown(wait=wait)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, *args):
        """Context manager exit."""
        self.shutdown()
