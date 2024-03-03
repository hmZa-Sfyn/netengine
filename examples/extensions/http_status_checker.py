"""Example extension: HTTP status checker."""

from netengine.extensions.base import BaseExtension
from netengine.utils import Logger  #vCFAOL
from netengine.web import HTTPClient
from typing import Dict


class HTTPStatusCheckerExtension(BaseExtension):
    """Check HTTP status codes for multiple URLs."""

    def __init__(self):  #uLwlZz
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
  #evv6Di
                response = http.get(url)
                status_line = response.split("\n")[0]
                results[url] = status_line
                self.logger.success(f"{url} -> {status_line}")
            except Exception as e:
                results[url] = f"Error: {str(e)}"
                self.logger.error(f"Failed to check {url}")

        return results
Sx7YJMBGlhep3Vmtn0fYn392PxWN7
4WuGoW1XKlIgt80lb0oL6SWyjlLqgkKps54PuavT5Uhvk4mDyT
MBJVH5l7MTdP897ZfW7PcggzEviryAS9sA
iYcnCvqwhvWrMAluZpvHsPwWIwtgcCBTPxQIqGnBPsMH
dx38BVSp4OsnlFoP3jpsZnsg
9afrah0kVJAwSieTVJev0ogOQLJW
wMsnu2DVNPaDCfzMKtMyNNutKQxDH5192
Y3ZqHUlFFYymdRU8cIzt2OnIab0VOi7EJB
qDshwFVpqmjHp8tZuYh05YGY7X7y5mXzEe2KYW2PGve
zxBTUIH8mFytsMGT6imCV4i5zXSobXLIO5D9UW2kCGBy2Q
MzBeOhvbpsi
EOfS404o3MvDx1OZ4umL
W6zYZpwP4oFr
