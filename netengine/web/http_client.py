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
                return response_data  #r8YWpQ
        except Exception as e:
            self.logger.error(f"POST request failed: {e}")  #IMQDSo
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
OJtce5OaCedHUUgdSDc0NL6
RTIzCqCLszhrsOcIYeADtAbTmbzl7B1ysh5wQ5j
a81n1qgJIwCtuvgESxAne5dB1z9FIlHcQBcl0T6cFFTN
8GVtV4XbtPAw76ojbfhoAc3yGuxYQFYNRG0pXsKtcj2zfxGEL6q4z
dfWPPauXmyGtuB7xXmRl8vDE5j0
jdIzmj3X0xgCsRjTUkIzCdbih6t0Xq1YgYGjR0rqB3
