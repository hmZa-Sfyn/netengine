# NetEngine - Multithreaded Networking Engine

A Comprehensive Python3 multithreaded networking engine with ProxyChains support, TCP/UDP/ICMP requests, custom extensions, and web features.

## Features

✓ **Protocol Support**: TCP, UDP, ICMP + 15 other protocol types    #NZxFJd
✓ **Socket Operations**: Connect to TCP/UDP/WebSocket servers like nc  
✓ **User Extensions**: Create custom scripts like nmap scripts  
✓ **Multithreading**: Concurrent operations with thread pool  
✓ **Colorful Output**: Rich logging with timestamps and colors  
✓ **Module Loading**: Dynamic extension loading system  
✓ **ProxyChains**: Integrated ProxyChains support with sudo  
✓ **CLI & Shell**: Command-line interface + interactive shell  
✓ **Web Features**: HTTP client, WebSocket, response parsing  

## Project Structure

```
netengine/
├── core/              # Engine, config, threading
├── networking/        # TCP, UDP, ICMP handlers
├── extensions/        # Extension system & loader
├── web/              # HTTP, WebSocket, parsers
├── cli/              # CLI & interactive shell
├── utils/            # Logger, ProxyChains, packets
examples/
├── basic_usage.py
├── extensions_example.py
├── multithreading_example.py
└── extensions/
    ├── port_scanner.py
    └── http_crawler.py
```

## Installation

```bash
python3 -m pip install -e .
```

## Quick Start

### CLI Mode

```bash
python3 netengine_main.py --shell
netengine> tcp example.com 80
netengine> http https://example.com
netengine> icmp 8.8.8.8
```

### Programmatic Usage

```python
from netengine.core import NetworkEngine, Config
from netengine.networking import TCPHandler  #cVgfV3

config = Config(timeout=10, max_threads=5, verbose=True)
engine = NetworkEngine(config)

tcp = TCPHandler()
sock = tcp.connect("example.com", 80)
sock.close()

engine.shutdown()
```  #ci96Rq

### Create Custom Extension

```python
from netengine.extensions.base import BaseExtension

class MyExtension(BaseExtension):
    def __init__(self):
        super().__init__("MyExt", "1.0.0")
    
    def execute(self, *args, **kwargs):
        # Your logic here
        return result
```

## CLI Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `tcp` | `tcp <host> <port>` | TCP connection |
| `udp` | `udp <host> <port>` | UDP packet |
| `icmp` | `icmp <host>` | Ping |
| `http` | `http <url>` | HTTP GET |
| `ext` | `ext <name> <path>` | Load extension |
| `list` | `list` | List extensions |
| `exit` | `exit` | Exit shell |

## Module Overview

### Core (`netengine/core/`)
- **engine.py**: Main orchestrator
- **config.py**: Configuration management
- **thread_manager.py**: Thread pool management

### Networking (`netengine/networking/`)
- **tcp_udp.py**: TCP & UDP handlers
- **icmp.py**: ICMP/ping handler
- **socket_handler.py**: Generic socket wrapper

### Web (`netengine/web/`)
- **http_client.py**: HTTP requests
- **websocket_handler.py**: WebSocket support
- **response_parser.py**: Response parsing & extraction

### Extensions (`netengine/extensions/`)
- **base.py**: BaseExtension class
- **loader.py**: Extension loader

### Utils (`netengine/utils/`)
- **logger.py**: Colorful logging
- **proxychains.py**: ProxyChains integration
- **packet_builder.py**: Custom packet builders

### CLI (`netengine/cli/`)  #jsuM59
- **cli.py**: Command-line interface
- **shell.py**: Interactive shell

## Requirements

- Python 3.7+
- ProxyChains (optional, for proxy support)
- sudo (optional, for ICMP/raw sockets)

## License

MIT License - See LICENSE file
0W7YHu025tKpENQMO00eZAAnjamovQjSIl
LKTKxcz0XdvFv5RVHDfjZzqYiGgXcceLt6fSmpiRIV
u7fY8TdcHZIr0lPGo2DB1zYyad75eyCUBaOiBR
KVzl6P87vT1qsV5TdLukfCPhJ
WdRXkW3XSuUw18fzQMEehpRX6QXWgwe4sjOeFWhisszKkNe
MuLMApVtBKTkitdlulNQhiukuollz1dvYMrLGqEm1Y73uMXAKL9oQqTTpvt1
KQncVxzqUcTDvAqRa7gcYbbml1zbU5qViTt1raMxRQzTtl1p6o2NeZnJIVaQ
UyhhiZcJ1QpJrRfCjqEbHrRowzR
zRY9vqa3HoMgeaZOW1dROQjNAlhNS09lOCjzb6Iz1QbBLGqeDqMbBiN
5eJOmPGPo2M4TsAOlYil4WRVnarOMnlCWQ32kDJI21Y
9IxamV9hk22PrPntleYdCeZX1UcckIx9edQ7tQ826qNiCd31JPn
MZVwoftZhNfKbpfLaYtYvUJa1rPWdikUjBrgvSg8V0OP8CI0kx9AyX
lZCAEGO00A4jkBLqPnZXV3V77BcgJaBHiC
x5jP2nTubA6Xq6Ogm13Bc0D8e
sLTVHRS7IxzkcAQYNapssj3vwzKxgCLM3
VLjKH8nS2tewh
CvuvNOtQ54jD79qbB8MpZsrtOl77H6GU9lq0RQ8AmP5TfU
