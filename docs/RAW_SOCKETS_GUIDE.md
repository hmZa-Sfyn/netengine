# NetEngine Raw Sockets & Packet Crafting Guide

## Table of Contents
1. [Understanding Raw Sockets](#understanding-raw-sockets)
2. [Socket Types](#socket-types)
3. [Packet Structure](#packet-structure)
4. [Platform-Specific Setup](#platform-specific-setup)
5. [Working with Advanced Packets](#working-with-advanced-packets)
6. [Examples](#examples)

## Understanding Raw Sockets

Raw sockets allow you to craft custom packets at the IP and transport layer levels. This is powerful for network testing, penetration testing, and security research.

### Key Concepts

- **Raw Socket**: Direct access to packet creation
- **Packet Crafting**: Building custom network packets
- **Checksum**: Verification of packet integrity
- **Headers**: IP and TCP/UDP headers

## Socket Types

### SOCK_STREAM (TCP)
```python
from netengine.networking import TCPHandler

tcp = TCPHandler()
socket = tcp.connect("example.com", 80)
socket.close()
```

### SOCK_DGRAM (UDP)
```python
from netengine.networking import UDPHandler

udp = UDPHandler()
sock = udp.send("example.com", 53, b"DNS Query")
data, addr = udp.receive(sock)
```

### SOCK_RAW (Raw Socket)
Requires root/admin privileges.

```python
import socket
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
```

## Packet Structure

### IP Header (20 bytes minimum)
```
┌──────────────────────────────────────┐
│ Version(4) │ IHL(4) │ ToS(8)         │
├──────────────────────────────────────┤
│ Total Length (16)                    │
├──────────────────────────────────────┤
│ Identification (16) │ Flags(3) │ Frag Offset (13) │
├──────────────────────────────────────┤
│ TTL (8) │ Protocol (8) │ Checksum (16) │
├──────────────────────────────────────┤
│ Source IP Address (32)               │
├──────────────────────────────────────┤
│ Destination IP Address (32)          │
└──────────────────────────────────────┘
```

### TCP Header (20 bytes minimum)
```
┌──────────────────────────────────────┐
│ Source Port (16) │ Dest Port (16)    │
├──────────────────────────────────────┤
│ Sequence Number (32)                 │
├──────────────────────────────────────┤
│ Acknowledgment Number (32)           │
├──────────────────────────────────────┤
│ Offset(4) │ Reserved(3) │ Flags(9)   │
├──────────────────────────────────────┤
│ Window Size (16) │ Checksum (16)     │
├──────────────────────────────────────┤
│ Urgent Pointer (16)                  │
└──────────────────────────────────────┘
```

## Platform-Specific Setup

### Linux/Unix

Raw sockets work directly with root privileges:

```bash
sudo python3 script.py
```

### Windows

Windows requires specific setup:

```python
import socket
import ctypes

# Enable raw socket support
if os.name == 'nt':
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass
```

### macOS

Similar to Linux but with some limitations:

```bash
sudo python3 script.py
```

## Working with Advanced Packets

### Build SYN Packet

```python
from netengine.utils.advanced_packets import AdvancedPacketBuilder

builder = AdvancedPacketBuilder()
packet = builder.build_syn_packet(
    src_ip="192.168.1.100",
    dst_ip="8.8.8.8",
    src_port=54321,
    dst_port=80
)
```

### Build FIN Packet

```python
packet = builder.build_fin_packet(
    src_ip="192.168.1.100",
    dst_ip="8.8.8.8",
    src_port=54321,
    dst_port=80
)
```

### Build RST Packet

```python
packet = builder.build_rst_packet(
    src_ip="192.168.1.100",
    dst_ip="8.8.8.8",
    src_port=54321,
    dst_port=80
)
```

### Build DNS Query

```python
packet = builder.build_dns_query("example.com", record_type="A")
```

## Examples

### Example 1: Simple Port Scan

```python
from netengine.core import NetworkEngine, Config
from netengine.networking import TCPHandler
from netengine.utils import Logger

logger = Logger()
tcp = TCPHandler(logger)

ports = [80, 443, 8080, 3000]
open_ports = []

for port in ports:
    try:
        sock = tcp.connect("localhost", port, timeout=1.0)
        open_ports.append(port)
        sock.close()
    except:
        pass

print(f"Open ports: {open_ports}")
```

### Example 2: Crafting SYN Packets

```python
import socket
from netengine.utils.advanced_packets import AdvancedPacketBuilder
from netengine.utils import Logger

logger = Logger()
builder = AdvancedPacketBuilder(logger)

# Build packet
packet = builder.build_syn_packet(
    src_ip="192.168.1.1",
    dst_ip="8.8.8.8",
    src_port=12345,
    dst_port=80
)

print(f"Packet size: {len(packet)} bytes")
```

### Example 3: Raw Socket Communication

```python
import socket

# Create raw socket (Linux/Unix only, requires root)
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

# Send packet
try:
    sock.sendto(packet, ("8.8.8.8", 0))
    print("Packet sent successfully")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()
```

### Example 4: Checksum Calculation

```python
def calculate_checksum(data: bytes) -> int:
    """Calculate IP/TCP checksum."""
    sum_val = 0
    count_to = (len(data) // 2) * 2
    
    for i in range(0, count_to, 2):
        w = (data[i] << 8) + data[i + 1]
        sum_val += w
    
    if count_to < len(data):
        sum_val += data[-1]
    
    sum_val = (sum_val >> 16) + (sum_val & 0xFFFF)
    sum_val += sum_val >> 16
    return ~sum_val & 0xFFFF
```

## Important Security Notes

⚠️ **WARNING**: Raw socket manipulation can be used for malicious purposes:
- SYN floods
- IP spoofing
- DDoS attacks
- Unauthorized network access

**ONLY USE FOR**:
- Authorized penetration testing
- Your own networks
- Educational purposes
- Security research with permission

**NEVER USE FOR**:
- Attacking networks you don't own
- Disrupting services
- Unauthorized access
- Any illegal activity

## Common Issues

### Permission Denied
```
OSError: [Errno 1] Operation not permitted
```
**Solution**: Run with root/admin privileges

### Module not found
```
ImportError: No module named 'netengine'
```
**Solution**: Install package: `pip install -e .`

### Windows raw socket limitation
Windows has stricter raw socket support. Use WSL or Linux for full raw socket access.

## Best Practices

1. Always check privileges before raw socket operations
2. Use proper error handling
3. Log all operations for audit trails
4. Never run on unauthorized networks
5. Validate inputs before packet creation
6. Use timeouts to prevent hanging
7. Close sockets properly
