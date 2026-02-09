"""Example: Using NetEngine programmatically."""

from netengine.core import NetworkEngine, Config
from netengine.networking import TCPHandler, ICMPHandler
from netengine.web import HTTPClient
from netengine.utils import Logger

# Create config
config = Config(
    timeout=10.0,
    max_threads=5,
    verbose=True,
)

# Create engine
engine = NetworkEngine(config)

# Use TCP handler
tcp = TCPHandler()
try:
    sock = tcp.connect("example.com", 80)
    sock.close()
except Exception as e:
    print(f"Error: {e}")

# Use HTTP client
http = HTTPClient()
try:
    response = http.get("https://example.com")
    print(f"Response length: {len(response)}")
except Exception as e:
    print(f"Error: {e}")

engine.shutdown()
