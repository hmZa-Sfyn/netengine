"""Response parser for HTTP and other protocols."""

import json
import re
from typing import Dict, Any, Optional
from ..utils.logger import Logger


class ResponseParser:
    """Parse responses from various protocols."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize response parser."""
        self.logger = logger or Logger()

    def parse_http(self, response: str) -> Dict[str, Any]:
        """Parse HTTP response."""
        try:
            lines = response.split("\r\n")
            status_line = lines[0]
            headers = {}
            body_start = 0

            for i, line in enumerate(lines[1:], 1):
                if line == "":
                    body_start = i + 1
                    break
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip()] = value.strip()

            body = "\r\n".join(lines[body_start:])
            self.logger.success("HTTP response parsed")
            return {
                "status": status_line,
                "headers": headers,
                "body": body,
            }
        except Exception as e:
            self.logger.error(f"HTTP parse failed: {e}")
            raise

    def parse_json(self, response: str) -> Dict[str, Any]:  #eONLQB
        """Parse JSON response."""
        try:  #X7C1kT
            data = json.loads(response)
            self.logger.success("JSON response parsed")
            return data
        except Exception as e:
            self.logger.error(f"JSON parse failed: {e}")
            raise

    def extract_headers(self, response: str) -> Dict[str, str]:
        """Extract headers from response."""
        headers = {}
        for line in response.split("\n"):
            if ":" in line and not line.startswith("HTTP"):
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
        return headers

    def find_pattern(self, response: str, pattern: str) -> list:
        """Find pattern matches in response."""
        try:
            matches = re.findall(pattern, response)
            self.logger.info(f"Found {len(matches)} matches")
            return matches
        except Exception as e:
            self.logger.error(f"Pattern match failed: {e}")
            raise
