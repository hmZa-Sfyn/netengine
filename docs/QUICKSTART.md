# NetEngine - Quick Start & Examples

## Quick Installation

```bash
cd netengine
pip install -r requirements.txt
python3 netengine_main.py --shell
```

## CLI Usage

### Start Interactive Shell
```bash
python3 netengine_main.py --shell
```

### Quick Commands
```bash
netengine> tcp google.com 80
netengine> http https://example.com
netengine> list
netengine> help
```

### Verbose Mode
```bash
python3 netengine_main.py --verbose --shell
```

## Code Examples

### Example 1: Simple TCP Connection

```python
from netengine.networking import TCPHandler
from netengine.utils import Logger

logger = Logger(verbose=True)
tcp = TCPHandler(logger)

try:
    sock = tcp.connect("example.com", 80)
    logger.success("Connected!")
    sock.close()
except Exception as e:
    logger.error("Connection failed", exc=e)
```

### Example 2: Port Scanning

```python
from netengine.core import ThreadManager
from netengine.networking import TCPHandler
from netengine.utils import Logger

logger = Logger()
tcp = TCPHandler(logger)
manager = ThreadManager(max_workers=10)

def scan_port(host, port):
    try:
        sock = tcp.connect(host, port, timeout=1.0)
        sock.close()
        return port
    except:
        return None

# Scan common ports
ports = [21, 22, 25, 80, 443, 3306, 5432, 8080]
results = manager.map_tasks(lambda p: scan_port("localhost", p), ports)
open_ports = [p for p in results if p is not None]

logger.success(f"Open ports: {open_ports}")
manager.shutdown()
```

### Example 3: HTTP Requests

```python
from netengine.web import HTTPClient, ResponseParser
from netengine.utils import Logger
import json

logger = Logger(verbose=True)
http = HTTPClient(logger)
parser = ResponseParser(logger)

# GET request
response = http.get("https://jsonplaceholder.typicode.com/users/1")
user = parser.parse_json(response)

logger.info(f"User: {user['name']} ({user['email']})")

# POST request
new_user = {"name": "Alice", "email": "alice@example.com"}
response = http.post(
    "https://jsonplaceholder.typicode.com/users",
    data=json.dumps(new_user).encode(),
    headers={"Content-Type": "application/json"}
)
```

### Example 4: Load and Use Extension

```python
from netengine.core import NetworkEngine, Config

# Create engine
config = Config(verbose=True, max_threads=5)
engine = NetworkEngine(config)

# Load extension
try:
    engine.load_extension("scanner", "./examples/extensions/port_scanner.py")
    
    # Execute extension
    open_ports = engine.execute_extension(
        "scanner",
        "localhost",
        [80, 443, 8080, 3000, 5000]
    )
    
    print(f"Found ports: {open_ports}")
except Exception as e:
    print(f"Error: {e}")
finally:
    engine.shutdown()
```

### Example 5: Custom Extension

Create `my_extension.py`:

```python
from netengine.extensions.base import BaseExtension
from netengine.utils import Logger


class MyCustomExtension(BaseExtension):
    """My custom extension."""
    
    def __init__(self):
        super().__init__("MyCustom", "1.0.0")
        self.logger = Logger()
    
    def execute(self, message: str):
        """Echo and return message."""
        self.logger.success(f"Message: {message}")
        return message.upper()
```

Use it:

```python
from netengine.core import NetworkEngine

engine = NetworkEngine()
engine.load_extension("mycustom", "./my_extension.py")
result = engine.execute_extension("mycustom", "hello world")
print(result)  # "HELLO WORLD"
engine.shutdown()
```

### Example 6: DNS Resolver

```python
import socket
from netengine.utils import Logger

logger = Logger()

domains = ["google.com", "github.com", "example.com"]

logger.info(f"Resolving {len(domains)} domains...")

for domain in domains:
    try:
        ip = socket.gethostbyname(domain)
        logger.success(f"{domain} -> {ip}")
    except socket.gaierror:
        logger.error(f"Failed to resolve {domain}")
```

### Example 7: Web Scraping

```python
from netengine.web import HTTPClient, ResponseParser
from netengine.utils import Logger

logger = Logger()
http = HTTPClient(logger)
parser = ResponseParser(logger)

# Fetch page
response = http.get("https://example.com")

# Extract information
emails = parser.find_pattern(
    response,
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
)
logger.success(f"Found {len(emails)} emails: {emails}")

# Extract links
links = parser.find_pattern(response, r'href=["\']([^"\']+)["\']')
logger.success(f"Found {len(links)} links")
```

### Example 8: Concurrent Operations

```python
from netengine.core import ThreadManager
from netengine.web import HTTPClient
from netengine.utils import Logger

logger = Logger()

def fetch_url(url):
    http = HTTPClient(logger)
    try:
        response = http.get(url, timeout=5)
        return len(response)
    except:
        return 0

# Fetch multiple URLs concurrently
urls = [
    "https://example.com",
    "https://google.com",
    "https://github.com"
]

manager = ThreadManager(max_workers=3)
results = manager.map_tasks(fetch_url, urls)

for url, size in zip(urls, results):
    logger.info(f"{url}: {size} bytes")

manager.shutdown()
```

### Example 9: Packet Crafting

```python
from netengine.utils.advanced_packets import AdvancedPacketBuilder
from netengine.utils import Logger

logger = Logger(verbose=True)
builder = AdvancedPacketBuilder(logger)

# Build SYN packet
packet = builder.build_syn_packet(
    src_ip="192.168.1.100",
    dst_ip="8.8.8.8",
    src_port=54321,
    dst_port=80
)

logger.success(f"Built packet: {len(packet)} bytes")

# Build DNS query
dns_packet = builder.build_dns_query("example.com", "A")
logger.success(f"Built DNS query: {len(dns_packet)} bytes")
```

### Example 10: Error Handling

```python
from netengine.networking import TCPHandler
from netengine.utils import Logger

logger = Logger()
tcp = TCPHandler(logger)

try:
    sock = tcp.connect("invalid.host.example", 80, timeout=2.0)
    sock.close()
except ConnectionRefusedError:
    logger.error("Connection refused")
except TimeoutError:
    logger.error("Connection timeout")
except OSError as e:
    logger.error(f"Socket error", exc=e)
except Exception as e:
    logger.error(f"Unknown error", exc=e)
```

## Using Include Files

### From Directory

```python
import sys
sys.path.insert(0, '/path/to/netengine')

from netengine.core import NetworkEngine
```

### From Package

```python
# After installation: pip install -e .
from netengine.core import NetworkEngine
from netengine.web import HTTPClient
```

## Performance Tips

1. **Use thread pools** for concurrent operations
2. **Set appropriate timeouts** to avoid hanging
3. **Cache HTTP responses** for repeated requests
4. **Use DNS resolution** in batch with threading
5. **Clean up resources** with context managers

```python
with ThreadManager(max_workers=10) as manager:
    results = manager.map_tasks(my_function, items)
    # Automatically shutdown when exiting
```

## Troubleshooting

### Import Error
```
ModuleNotFoundError: No module named 'netengine'
```
**Solution**: Run `pip install -e .` from project root

### Permission Denied
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Run with sudo for raw sockets: `sudo python3 script.py`

### Connection Refused
```
ConnectionRefusedError: [Errno 111] Connection refused
```
**Solution**: Check if service is running on target port

### Timeout
```
socket.timeout: _ssl.c:1055: The handshake operation timed out
```
**Solution**: Increase timeout: `http.timeout = 30`

## Resources

- **Documentation**: See `/docs/` folder
- **Examples**: See `/examples/` folder
- **Extensions**: See `/examples/extensions/` folder
- **Raw Sockets**: Read `docs/RAW_SOCKETS_GUIDE.md`
- **Web Features**: Read `docs/WEB_FEATURES_GUIDE.md`
- **Extension Dev**: Read `docs/EXTENSION_DEVELOPMENT.md`

## Next Steps

1. Explore `examples/` directory
2. Create custom extensions
3. Combine tools for complex workflows
4. Integrate with existing tools
5. Build security tools
6. Contribute back!
