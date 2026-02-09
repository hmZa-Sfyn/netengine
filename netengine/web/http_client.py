"""HTTP client for web requests."""

import urllib.request
import urllib.error
from typing import Dict, Optional
from ..utils.logger import Logger


class HTTPClient:
    """HTTP request client."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize HTTP client."""
        self.logger = logger or Logger()
        self.timeout = 10.0

    def get(self, url: str, headers: Optional[Dict] = None) -> str:
        """Perform GET request."""
        try:
            req = urllib.request.Request(url)
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = response.read().decode()
                self.logger.success(f"GET {url}")
                return data
        except Exception as e:
            self.logger.error(f"GET request failed: {e}")
            raise

    def post(self, url: str, data: bytes, headers: Optional[Dict] = None) -> str:
        """Perform POST request."""
        try:
            req = urllib.request.Request(url, data=data, method="POST")
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode()
                self.logger.success(f"POST {url}")
                return response_data
        except Exception as e:
            self.logger.error(f"POST request failed: {e}")
            raise

    def head(self, url: str, headers: Optional[Dict] = None) -> Dict:
        """Perform HEAD request."""
        try:
            req = urllib.request.Request(url, method="HEAD")
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                self.logger.success(f"HEAD {url}")
                return dict(response.headers)
        except Exception as e:
            self.logger.error(f"HEAD request failed: {e}")
            raise
