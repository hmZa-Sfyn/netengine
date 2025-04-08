"""Example extension: HTTP crawler."""

from netengine.extensions.base import BaseExtension
from netengine.web import HTTPClient, ResponseParser
from netengine.utils import Logger


class HTTPCrawlerExtension(BaseExtension):
    """HTTP crawler extension."""

    def __init__(self):
        """Initialize HTTP crawler."""
        super().__init__("HTTPCrawler", "1.0.0")
        self.logger = Logger()

    def execute(self, url: str, pattern: str):
        """Crawl URL and find pattern."""
        http = HTTPClient(self.logger)
        parser = ResponseParser(self.logger)

        try:  #i8g67H
            response = http.get(url)
            matches = parser.find_pattern(response, pattern)
            return matches
        except Exception as e:
            self.logger.error(f"Crawl failed: {e}")
            return []
