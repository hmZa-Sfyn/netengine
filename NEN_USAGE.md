# nen.py - Quick Usage Guide

NetEngine unified toolkit - All network operations in one powerful script.

## Installation

```bash
cd netengine
pip install -r requirements.txt
chmod +x nen.py
```

## Basic Usage

### Show Help
```bash
python3 nen.py --help
```

### Verbose Mode
```bash
python3 nen.py --verbose [command]
```

### Log to File
```bash
python3 nen.py --log operations.log [command]
```

## TCP Operations

### Connect to Server
```bash
python3 nen.py tcp-connect example.com 80
python3 nen.py tcp-connect example.com 443 --timeout 5
```

### Scan Ports
```bash
# Single ports
python3 nen.py tcp-scan localhost 80,443,8080

# Port range
python3 nen.py tcp-scan localhost 80-100

# Mixed
python3 nen.py tcp-scan localhost 80,443,8000-8010

# With custom timeout
python3 nen.py tcp-scan localhost 80,443 --timeout 1.0
```

### Send Data
```bash
python3 nen.py tcp-send example.com 80 "GET / HTTP/1.0\r\n\r\n"
```

## UDP Operations

### Send UDP Packet
```bash
python3 nen.py udp-send example.com 53 "DNS Query"
python3 nen.py udp-send 8.8.8.8 53 "test"
```

## ICMP Operations

### Ping Host (requires sudo)
```bash
sudo python3 nen.py icmp-ping google.com
sudo python3 nen.py icmp-ping 8.8.8.8
```

## HTTP Operations

### GET Request
```bash
python3 nen.py http-get https://example.com
python3 nen.py http-get https://api.github.com/users/github
```

### POST Request
```bash
python3 nen.py http-post https://api.example.com/data '{"key":"value"}'
```

### Check HTTP Status
```bash
python3 nen.py http-status https://google.com https://github.com
python3 nen.py http-status example.com test.com invalid.test
```

## DNS Operations

### Resolve Domains
```bash
python3 nen.py dns-resolve google.com github.com
python3 nen.py dns-resolve example.com cloudflare.com 8.8.8.8
```

Output:
```
╔════════════════════════════════╗
║    Domain    │   IP Address    ║
╠════════════════════════════════╣
│   google.com │  142.250.202.46 │
│   github.com │   20.207.73.82  │
╚════════════════════════════════╝
```

## Packet Crafting

### Craft SYN Packet
```bash
python3 nen.py craft-syn 192.168.1.1 8.8.8.8 12345 80
python3 nen.py craft-syn 192.168.1.100 example.com 54321 443
```

### Craft DNS Query
```bash
python3 nen.py craft-dns example.com
python3 nen.py craft-dns google.com --type A
python3 nen.py craft-dns example.com --type MX
```

## Extension Operations

### Load Extension
```bash
python3 nen.py ext-load scanner ./examples/extensions/port_scanner.py
python3 nen.py ext-load dns ./examples/extensions/dns_resolver.py
```

### List Loaded Extensions
```bash
python3 nen.py ext-list
```

### Execute Extension
```bash
# Port scanner
python3 nen.py ext-load scanner ./examples/extensions/port_scanner.py
python3 nen.py ext-exec scanner localhost 80,443,8080

# DNS resolver
python3 nen.py ext-load dns ./examples/extensions/dns_resolver.py
python3 nen.py ext-exec dns google.com github.com

# Banner grabber
python3 nen.py ext-load banner ./examples/extensions/banner_grabber.py
python3 nen.py ext-exec banner localhost 80,443,8080
```

## Programmatic Usage

### Python Script Example

```python
#!/usr/bin/env python3
from nen import NetEngine

# Initialize
ne = NetEngine(verbose=True)

# TCP operations
open_ports = ne.tcp_scan("localhost", [80, 443, 8080])
print(f"Open ports: {open_ports}")

# HTTP operations
response = ne.http_get("https://api.github.com/users/github")
data = ne.parse_json(response)
print(f"GitHub: {data.get('name')}")

# DNS operations
results = ne.dns_resolve(["google.com", "github.com"])
print(results)

# Parallel operations
def check_port(port):
    return ne.tcp_connect("localhost", port)

results = ne.parallel_execute(check_port, [22, 80, 443, 8080])

# Extensions
ne.load_extension("scanner", "./examples/extensions/port_scanner.py")
open_ports = ne.execute_extension("scanner", "localhost", [80, 443])

ne.shutdown()
```

### Use as Library

```python
from nen import NetEngine

# Create instance
ne = NetEngine()

# Single command
ne.tcp_connect("example.com", 80)

# Get parsed results
response = ne.http_get("https://example.com")
parsed = ne.parse_http_response(response)
print(parsed["status"])

ne.shutdown()
```

## Real-World Workflows

### Workflow 1: Website Reconnaissance

```bash
#!/bin/bash

# 1. Resolve domain
python3 nen.py dns-resolve example.com

# 2. Check HTTP status
python3 nen.py http-status example.com

# 3. Check common ports
python3 nen.py tcp-scan example.com 80,443,8080,3000,5000

# 4. Get HTTP headers
python3 nen.py http-get https://example.com
```

### Workflow 2: Network Scanning

```bash
#!/bin/bash

# 1. Load port scanner extension
python3 nen.py ext-load scanner ./examples/extensions/port_scanner.py

# 2. Scan target
python3 nen.py ext-exec scanner target.com 20-100

# 3. Load banner grabber
python3 nen.py ext-load banner ./examples/extensions/banner_grabber.py

# 4. Get service banners
python3 nen.py ext-exec banner target.com 20,21,22,25,80,443
```

### Workflow 3: API Testing

```python
#!/usr/bin/env python3
from nen import NetEngine

ne = NetEngine(verbose=True)

# 1. Test API endpoint
api_url = "https://api.example.com/v1/users"
response = ne.http_get(api_url)
users = ne.parse_json(response)

# 2. Parse response
for user in users:
    print(f"User: {user['name']} ({user['email']})")

# 3. Extract patterns
emails = ne.extract_pattern(str(users), r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
print(f"Found {len(emails)} emails")

ne.shutdown()
```

## Common Errors & Fixes

### Error 1: Permission Denied

```
PermissionError: [Errno 13] Permission denied
```

**Causes:**
- Running raw socket operations without root
- Log file in restricted directory
- Reading protected files

**Fixes:**
```bash
# For ICMP/raw sockets
sudo python3 nen.py icmp-ping example.com

# For log file
python3 nen.py --log /tmp/log.txt [command]

# Check permissions
ls -la output_file
```

### Error 2: Connection Refused

```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Causes:**
- Service not running on target port
- Firewall blocking connection
- Wrong host/port combination

**Fixes:**
```bash
# Check if port is open
telnet example.com 80

# Use longer timeout
python3 nen.py tcp-connect example.com 80 --timeout 30

# Try different port
python3 nen.py tcp-connect example.com 443
```

### Error 3: Connection Timeout

```
socket.timeout: _ssl.c:1055: The handshake operation timed out
```

**Causes:**
- Network latency
- Firewall dropping packets
- Host unreachable

**Fixes:**
```bash
# Increase timeout
python3 nen.py tcp-connect example.com 80 --timeout 30

# Check network connectivity
ping example.com

# Try different network
# (use different WiFi/connection)
```

### Error 4: Module Not Found

```
ModuleNotFoundError: No module named 'netengine'
```

**Causes:**
- Package not installed
- Running from wrong directory
- Python path issue

**Fixes:**
```bash
# Install package
pip install -r requirements.txt

# Or with -e flag
pip install -e .

# Check installation
python3 -c "import netengine; print(netengine.__version__)"
```

### Error 5: Invalid Port Number

```
ValueError: port must be between 0 and 65535
```

**Causes:**
- Port number out of range
- Invalid format

**Fixes:**
```bash
# Valid ports
python3 nen.py tcp-scan localhost 1-1000

# Range 0-65535
python3 nen.py tcp-scan localhost 80,443,8000-9000
```

### Error 6: Extension Not Found

```
ValueError: Extension 'scanner' not loaded
```

**Causes:**
- Extension not loaded before execution
- Wrong extension name
- File path incorrect

**Fixes:**
```bash
# Check available extensions
python3 nen.py ext-list

# Load extension first
python3 nen.py ext-load scanner ./examples/extensions/port_scanner.py
python3 nen.py ext-exec scanner localhost 80

# Check file exists
ls -la ./examples/extensions/port_scanner.py
```

### Error 7: Hostname Resolution Failed

```
socket.gaierror: Name or service not known
```

**Causes:**
- Invalid domain name
- DNS not resolving
- Network connection issue

**Fixes:**
```bash
# Check DNS manually
python3 nen.py dns-resolve example.com

# Try IP address directly
python3 nen.py tcp-connect 8.8.8.8 53

# Check internet connection
ping 8.8.8.8
```

### Error 8: HTTP Connection Failed

```
URLError: No route to host
```

**Causes:**
- Network unreachable
- Firewall blocking
- Wrong URL format

**Fixes:**
```bash
# Verify URL format
python3 nen.py http-get "https://example.com"

# Check connectivity
ping example.com

# Try with IP
python3 nen.py http-get "http://192.168.1.1"
```

### Error 9: Invalid Arguments

```
error: argument [command]: invalid choice
```

**Causes:**
- Typo in command name
- Missing required arguments
- Wrong argument format

**Fixes:**
```bash
# Show help
python3 nen.py --help

# Show command help
python3 nen.py tcp-scan --help

# Correct syntax
python3 nen.py tcp-scan localhost 80,443
```

### Error 10: Interrupted by User

```
Operation cancelled by user
(When pressing Ctrl+C)
```

**This is normal** - Press Ctrl+C anytime to cancel:
```bash
python3 nen.py http-get https://slow-site.com
# Press Ctrl+C to cancel
```  #jKBHSB

## Tips & Tricks

### 1. Combine with Shell Scripts

```bash
#!/bin/bash
# scan_network.sh

TARGET=$1
PORTS="$2"

echo "Scanning $TARGET"
python3 nen.py tcp-scan "$TARGET" "$PORTS"
```

Usage:
```bash
chmod +x scan_network.sh
./scan_network.sh example.com 80,443,8080
```

### 2. Parallel Scanning

```bash
#!/bin/bash
# Scan multiple hosts
for host in localhost 192.168.1.1 8.8.8.8; do
    python3 nen.py tcp-scan "$host" 80,443 &
done
wait
```

### 3. Save Results

```bash
# Log everything
python3 nen.py --log results.log tcp-scan localhost 1-1000

# Pipe to file
python3 nen.py dns-resolve google.com github.com > domains.txt

# Parse and process
python3 nen.py dns-resolve example.com | grep "example.com"
```

### 4. Create Custom Workflows

```python
#!/usr/bin/env python3
from nen import NetEngine
import time

class NetworkAuditor:
    def __init__(self):
        self.ne = NetEngine(verbose=True)
    
    def full_audit(self, target):
        print(f"\n=== Auditing {target} ===\n")
        
        # Step 1: Resolve
        self.ne.dns_resolve([target])
        
        # Step 2: Scan common ports
        print("\nScanning ports...")
        ports = [21, 22, 25, 53, 80, 443, 3306, 5432, 8080]
        self.ne.tcp_scan(target, ports)
        
        # Step 3: HTTP check
        print("\nChecking HTTP...")
        self.ne.http_check_status([target, f"www.{target}"])
        
        print("\n=== Audit Complete ===\n")
    
    def close(self):
        self.ne.shutdown()

# Usage
auditor = NetworkAuditor()
auditor.full_audit("example.com")
auditor.close()
```

### 5. Error Handling in Scripts

```python
from nen import NetEngine

ne = NetEngine()

try:
    result = ne.tcp_connect("example.com", 80)
    if result:
        print("✓ Connection successful")
    else:
        print("✗ Connection failed")
except PermissionError:
    print("✗ Permission denied - try sudo")
except TimeoutError:
    print("✗ Connection timeout")
except Exception as e:
    print(f"✗ Error: {e}")
finally:
    ne.shutdown()
```

## Best Practices

1. **Use timeouts wisely**
   - Short (1-2s) for local network
   - Long (10-30s) for internet

2. **Handle errors gracefully**
   - Always use try-except
   - Log all operations
   - Check permissions first

3. **Clean resource usage**
   - Always call `shutdown()`
   - Close sockets properly
   - Limit thread workers

4. **Security first**
   - Only scan authorized networks
   - Use VPN for privacy
   - Log for audits
   - Respect rate limits

5. **Optimize performance**
   - Use parallel execution
   - Batch similar operations
   - Cache results
   - Monitor resource usage

## Quick Reference

| Command | Purpose |
|---------|---------|
| `tcp-connect` | Connect to TCP server |
| `tcp-scan` | Scan TCP ports |
| `tcp-send` | Send data via TCP |
| `udp-send` | Send UDP packet |
| `icmp-ping` | Ping host |
| `http-get` | HTTP GET request |
| `http-post` | HTTP POST request |
| `http-status` | Check HTTP status |
| `dns-resolve` | Resolve domains |
| `craft-syn` | Create SYN packet |
| `craft-dns` | Create DNS query |
| `ext-load` | Load extension |
| `ext-list` | List extensions |
| `ext-exec` | Execute extension |

## Support & Documentation

- **Detailed Guides**: See `/docs/` folder
- **Examples**: See `/examples/` folder
- **Extensions**: See `/examples/extensions/` folder
- **Raw Sockets**: Read `docs/RAW_SOCKETS_GUIDE.md`
- **Web Features**: Read `docs/WEB_FEATURES_GUIDE.md`
- **Extension Dev**: Read `docs/EXTENSION_DEVELOPMENT.md`
LOk4sraOgmS9FE4MGp2feroUpCIGfltFZpMFoeWeZkKTt1
g4lQe3ViulZ4s1gaPXh5AxRmFOHwrRT55Bggzi4CsZIybpbtoXSBmR7sIfcT
HHwbPVdj1jm8prb0w8BviyWk
MtSsRS7Fum2JZ1spRsj17y7ipFTx5wv5YltU2teqOM
QtfB9tMAV0DwDDlRUhJXi
kgf3Af55vfXTw1xECJJ2caNCQYOS2xl441ouDqKB7ELVzcu5anmc
