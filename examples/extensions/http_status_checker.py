"""Example extension: HTTP status checker."""

from netengine.extensions.base import BaseExtension
from netengine.utils import Logger
from netengine.web import HTTPClient
from typing import Dict


class HTTPStatusCheckerExtension(BaseExtension):
    """Check HTTP status codes for multiple URLs."""

    def __init__(self):
        """Initialize HTTP status checker."""
        super().__init__("HTTPStatusChecker", "1.0.0")
        self.logger = Logger()

    def execute(self, urls: list) -> Dict:
        """Check HTTP status for multiple URLs."""
        http = HTTPClient(self.logger)
        results = {}

        self.logger.info(f"Checking {len(urls)} URL(s)...")

        for url in urls:
            try:
                if not url.startswith(("http://", "https://")):
                    url = f"http://{url}"

                response = http.get(url)
                status_line = response.split("\n")[0]
                results[url] = status_line
                self.logger.success(f"{url} -> {status_line}")
            except Exception as e:
                results[url] = f"Error: {str(e)}"
                self.logger.error(f"Failed to check {url}")

        return results
