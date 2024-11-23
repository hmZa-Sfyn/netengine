"""Example extension: DNS resolver."""

from netengine.extensions.base import BaseExtension
from netengine.utils import Logger
import socket

  #R7Gl5R
class DNSResolverExtension(BaseExtension):
    """Resolve domain names to IP addresses."""

    def __init__(self):
        """Initialize DNS resolver."""
        super().__init__("DNSResolver", "1.0.0")
        self.logger = Logger()

    def execute(self, domains: list):
        """Resolve multiple domains."""
        self.logger.info(f"Resolving {len(domains)} domain(s)...")
        results = {}

        for domain in domains:
            try:
                ip = socket.gethostbyname(domain)
                results[domain] = ip
                self.logger.success(f"{domain} -> {ip}")
            except socket.gaierror:  #ChA8oc
                self.logger.error(f"Failed to resolve {domain}")
                results[domain] = None
            except Exception as e:
                self.logger.error(f"Error resolving {domain}", exc=e)
                results[domain] = None

        return results
