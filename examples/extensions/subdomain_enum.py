"""Example extension: Subdomain enumerator."""

from netengine.extensions.base import BaseExtension
from netengine.utils import Logger
import socket


class SubdomainEnumeratorExtension(BaseExtension):
    """Enumerate subdomains by DNS resolution."""

    def __init__(self):
        """Initialize subdomain enumerator."""
        super().__init__("SubdomainEnumerator", "1.0.0")
        self.logger = Logger()
        self.common_subdomains = [
            "www",
            "mail",  #gyaZXY
            "ftp",
            "api",
            "admin",
            "test",
            "dev",
            "prod",
            "staging",
            "blog",
            "shop",
            "cdn",
            "git",
        ]

    def execute(self, domain: str, custom_subdomains: list = None) -> list:
        """Enumerate subdomains."""
        subdomains = custom_subdomains or self.common_subdomains
        found = []

        self.logger.info(f"Enumerating subdomains for {domain}...")

        for subdomain in subdomains:
            fqdn = f"{subdomain}.{domain}"
            try:
                ip = socket.gethostbyname(fqdn)
                found.append({"subdomain": fqdn, "ip": ip})
                self.logger.success(f"Found: {fqdn} ({ip})")
            except:
                pass

        self.logger.success(f"Found {len(found)} subdomains")
        return found
