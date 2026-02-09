# NetEngine Extension Development Guide

## Table of Contents
1. [Creating Custom Extensions](#creating-custom-extensions)
2. [Extension Structure](#extension-structure)
3. [Using NetEngine Components](#using-netengine-components)
4. [Real-World Examples](#real-world-examples)
5. [Testing Extensions](#testing-extensions)
6. [Best Practices](#best-practices)

## Creating Custom Extensions

### Basic Extension Template

```python
from netengine.extensions.base import BaseExtension
from netengine.utils import Logger


class MyExtension(BaseExtension):
    """Description of what your extension does."""
    
    def __init__(self):
        """Initialize extension."""
        super().__init__("MyExtension", "1.0.0")
        self.logger = Logger()
        self.metadata = {
            "author": "Your Name",
            "description": "Extension description",
            "tags": ["networking", "testing"]
        }
    
    def execute(self, *args, **kwargs):
        """Execute extension logic."""
        self.logger.info("Extension executing...")
        # Your logic here
        return result
```

## Extension Structure

### Required Methods

1. `__init__()`: Initialize extension
2. `execute(*args, **kwargs)`: Main logic

### Optional Attributes

- `metadata`: Dictionary with extension info
- `logger`: Logger instance for output
- `version`: Extension version

## Using NetEngine Components

### 1. Network Operations

```python
from netengine.extensions.base import BaseExtension
from netengine.networking import TCPHandler, UDPHandler, ICMPHandler


class NetworkExtension(BaseExtension):
    def __init__(self):
        super().__init__("NetworkExt", "1.0.0")
        self.tcp = TCPHandler()
        self.udp = UDPHandler()
        self.icmp = ICMPHandler()
    
    def execute(self, host, port):
        # Test TCP connection
        try:
            sock = self.tcp.connect(host, port)
            sock.close()
            return "TCP open"
        except:
            return "TCP closed"
```

### 2. Threading Operations

```python
from netengine.extensions.base import BaseExtension
from netengine.core import ThreadManager


class ParallelExtension(BaseExtension):
    def __init__(self):
        super().__init__("ParallelExt", "1.0.0")
        self.manager = ThreadManager(max_workers=5)
    
    def execute(self, items):
        results = self.manager.map_tasks(self.process_item, items)
        self.manager.shutdown()
        return results
    
    def process_item(self, item):
        return item.upper()
```

### 3. Web Operations

```python
from netengine.extensions.base import BaseExtension
from netengine.web import HTTPClient, ResponseParser


class WebExtension(BaseExtension):
    def __init__(self):
        super().__init__("WebExt", "1.0.0")
        self.http = HTTPClient()
        self.parser = ResponseParser()
    
    def execute(self, url):
        response = self.http.get(url)
        data = self.parser.parse_json(response)
        return data
```

### 4. Packet Crafting

```python
from netengine.extensions.base import BaseExtension
from netengine.utils.advanced_packets import AdvancedPacketBuilder


class PacketExtension(BaseExtension):
    def __init__(self):
        super().__init__("PacketExt", "1.0.0")
        self.builder = AdvancedPacketBuilder()
    
    def execute(self, src_ip, dst_ip, port):
        packet = self.builder.build_syn_packet(src_ip, dst_ip, 12345, port)
        return len(packet)
```

## Real-World Examples

### Example 1: Port Scanner Extension

```python
from netengine.extensions.base import BaseExtension
from netengine.networking import TCPHandler


class PortScannerExt(BaseExtension):
    def __init__(self):
        super().__init__("PortScanner", "1.0.0")
        self.logger = Logger()
    
    def execute(self, host: str, ports: list, timeout: float = 2.0):
        """Scan ports on target host."""
        tcp = TCPHandler(self.logger)
        open_ports = []
        
        self.logger.info(f"Scanning {host} ({len(ports)} ports)...")
        
        for port in ports:
            try:
                sock = tcp.connect(host, port, timeout=timeout)
                open_ports.append(port)
                sock.close()
            except:
                pass
        
        self.logger.success(f"Found {len(open_ports)} open ports")
        return open_ports
```

**Usage:**
```python
from netengine.core import NetworkEngine, Config

engine = NetworkEngine(Config(verbose=True))
engine.load_extension("scanner", "./port_scanner.py")

# Execute extension
open_ports = engine.execute_extension(
    "scanner",
    "localhost",
    [80, 443, 8080, 3000, 5000]
)
print(open_ports)
```

### Example 2: Website Crawler

```python
from netengine.extensions.base import BaseExtension
from netengine.web import HTTPClient, ResponseParser
import re


class WebCrawlerExt(BaseExtension):
    def __init__(self):
        super().__init__("WebCrawler", "1.0.0")
        self.logger = Logger()
    
    def execute(self, url: str):
        """Crawl website and extract information."""
        http = HTTPClient(self.logger)
        parser = ResponseParser(self.logger)
        
        self.logger.info(f"Crawling {url}...")
        
        try:
            response = http.get(url)
            
            # Extract various data
            result = {
                "url": url,
                "emails": parser.find_pattern(response, r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
                "links": parser.find_pattern(response, r'href=["\']([^"\']+)["\']'),
                "headers": parser.extract_headers(response)
            }
            
            self.logger.success(f"Crawl complete")
            return result
        except Exception as e:
            self.logger.error(f"Crawl failed", exc=e)
            return None
```

### Example 3: Multi-threaded DNS Resolver

```python
from netengine.extensions.base import BaseExtension
from netengine.core import ThreadManager
import socket


class DNSResolverExt(BaseExtension):
    def __init__(self):
        super().__init__("DNSResolver", "1.0.0")
        self.logger = Logger()
        self.manager = ThreadManager(max_workers=10)
    
    def execute(self, domains: list):
        """Resolve multiple domains in parallel."""
        self.logger.info(f"Resolving {len(domains)} domains...")
        
        results = self.manager.map_tasks(self.resolve_domain, domains)
        self.manager.shutdown()
        
        return dict(zip(domains, results))
    
    def resolve_domain(self, domain):
        try:
            ip = socket.gethostbyname(domain)
            self.logger.success(f"{domain} -> {ip}")
            return ip
        except:
            return None
```

## Testing Extensions

### Unit Test

```python
import unittest
from netengine.core import NetworkEngine, Config


class TestPortScanner(unittest.TestCase):
    def setUp(self):
        self.engine = NetworkEngine(Config(verbose=False))
        self.engine.load_extension("scanner", "./examples/extensions/port_scanner.py")
    
    def test_scan_localhost(self):
        result = self.engine.execute_extension("scanner", "localhost", [80, 443])
        self.assertIsInstance(result, list)
    
    def tearDown(self):
        self.engine.shutdown()


if __name__ == "__main__":
    unittest.main()
```

### Manual Testing

```python
from netengine.core import NetworkEngine, Config

# Test 1: Load extension
engine = NetworkEngine(Config(verbose=True))

try:
    engine.load_extension("test", "./examples/extensions/port_scanner.py")
    print("✓ Extension loaded")
except Exception as e:
    print(f"✗ Load failed: {e}")

# Test 2: Execute extension
try:
    result = engine.execute_extension("test", "localhost", [22, 80, 443])
    print(f"✓ Extension executed: {result}")
except Exception as e:
    print(f"✗ Execution failed: {e}")

engine.shutdown()
```

## Best Practices

### 1. Error Handling

```python
def execute(self, *args, **kwargs):
    try:
        # Your logic
        pass
    except KeyboardInterrupt:
        self.logger.warning("Interrupted by user")
        return None
    except Exception as e:
        self.logger.error(f"Operation failed", exc=e)
        return None
```

### 2. Logging

```python
self.logger.info("Starting operation")
self.logger.success("Operation successful")
self.logger.warning("Warning message")
self.logger.error("Error message", exc=exception)
self.logger.debug("Debug info")  # Only in verbose mode
```

### 3. Resource Management

```python
def execute(self):
    manager = ThreadManager(max_workers=5)
    try:
        # Do work
        pass
    finally:
        manager.shutdown()
```

### 4. Type Hints

```python
from typing import List, Dict, Optional

def execute(
    self,
    hosts: List[str],
    ports: List[int],
    timeout: float = 10.0
) -> Dict:
    """Execute with type hints."""
    pass
```

### 5. Documentation

```python
class MyExtension(BaseExtension):
    """
    Brief description.
    
    Longer description of what the extension does
    and how it works.
    """
    
    def execute(self, param1: str, param2: int) -> dict:
        """
        Execute the extension.
        
        Args:
            param1: Description of param1
            param2: Description of param2
        
        Returns:
            Dictionary with results
        """
        pass
```

## Security Notes

⚠️ **Important**: When developing extensions:

1. **Input Validation**: Always validate user inputs
2. **Authorization**: Check for proper permissions
3. **Logging**: Log sensitive operations
4. **Error Messages**: Don't expose sensitive info
5. **Resource Limits**: Prevent infinite loops
6. **Timeouts**: Always set operation timeouts

### Security Template

```python
class SecureExtension(BaseExtension):
    def execute(self, target: str, port: int):
        # Validate inputs
        if not isinstance(port, int) or not (0 < port < 65536):
            self.logger.error("Invalid port number")
            return None
        
        if not target:
            self.logger.error("Target cannot be empty")
            return None
        
        # Check permissions
        if not self.has_permission():
            self.logger.error("Insufficient permissions")
            return None
        
        # Execute with timeout
        try:
            result = self._execute_with_timeout(target, port, timeout=10)
            self.logger.success("Operation completed")
            return result
        except Exception as e:
            self.logger.error("Operation failed", exc=e)
            return None
```

## Sharing Extensions

1. Create a new repository
2. Add proper documentation
3. Include examples and tests
4. Follow code style guidelines
5. Add LICENSE file
6. Submit to NetEngine community
