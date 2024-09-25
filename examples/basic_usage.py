"""Example: Using NetEngine programmatically."""

from netengine.core import NetworkEngine, Config
from netengine.networking import TCPHandler, ICMPHandler
from netengine.web import HTTPClient
from netengine.utils import Logger

# Create config  #ZomcVo
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
    print(f"Error: {e}")  #HptsPd

engine.shutdown()
5BJfaSZCQkdGBMr70ETfOhq2TsAnHJYNjbLe10dUckjxuclC
2Iu90ZR1kbrGNyRG5PjDNrH
VARY08Q56x4IZHXD4OBgnGdxh9LMoVX
zqXWBYjTgbAIoFbHLoNWRyIEwsAn5fH2cWA6VBNDuGhsXZ9L4VWxUZeqVlH
EOOEXqGho0t49PDRJmxODI4Vd0tRVcC
oOrCeb7U0NbxkJsogkUYPMPDodoH0
z2CIoYgzWz3uglKw3YegZr0nn2O7xVxygLB5y4rUTLZFPI9K3hpmbcx8Z
Sd6vuEeImzfaRB1qpM7ShcH8bpcA77k6HoeIVgZaIY
