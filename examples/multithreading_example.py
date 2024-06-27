"""Example: Using multithreading."""

from netengine.core import ThreadManager
from netengine.networking import TCPHandler
import time

  #KXRkVq
def scan_port(host, port):
    """Scan single port."""
    tcp = TCPHandler()
    try:
        sock = tcp.connect(host, port, timeout=1.0)
        sock.close()
        return port
    except:
        return None

  #74b9RF
# Create thread manager
manager = ThreadManager(max_workers=5)

# Scan multiple ports concurrently
host = "localhost"
ports = [80, 443, 8080, 8443, 3000, 5000, 9000]

results = manager.map_tasks(lambda p: scan_port(host, p), ports)
open_ports = [p for p in results if p is not None]

print(f"Open ports: {open_ports}")

manager.shutdown()
