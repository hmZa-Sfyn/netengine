# NetEngine Web Features Guide

## Table of Contents
1. [HTTP Client](#http-client)
2. [WebSocket Support](#websocket-support)
3. [Response Parsing](#response-parsing)
4. [Request Building](#request-building)
5. [Examples](#examples)
6. [Advanced Usage](#advanced-usage)

## HTTP Client

### Basic HTTP Requests

#### GET Request
```python
from netengine.web import HTTPClient
from netengine.utils import Logger

logger = Logger()
http = HTTPClient(logger)
http.timeout = 10.0

# Simple GET
response = http.get("https://api.example.com/users")
print(response)
```

#### POST Request
```python
import json

data = json.dumps({"name": "John", "email": "john@example.com"})
response = http.post(
    "https://api.example.com/users",
    data=data.encode(),
    headers={"Content-Type": "application/json"}
)
```

#### HEAD Request
```python
headers = http.head("https://example.com")
print(f"Server: {headers.get('server')}")
print(f"Content-Type: {headers.get('content-type')}")
```

### Custom Headers

```python
headers = {
    "User-Agent": "NetEngine/1.0",
    "Authorization": "Bearer token123",
    "X-Custom-Header": "custom-value"
}

response = http.get("https://api.example.com/data", headers=headers)
```

## WebSocket Support

### Connect to WebSocket

```python
from netengine.web import WebSocketHandler

ws = WebSocketHandler()
ws.connect("echo.websocket.org", port=80)

# Send data
ws.send("Hello WebSocket")

# Receive data
response = ws.receive()
print(response)

# Close connection
ws.close()
```

### WebSocket Chat Example

```python
import threading

def receiver_thread(ws):
    while True:
        try:
            msg = ws.receive()
            print(f"[Received]: {msg}")
        except:
            break

ws = WebSocketHandler()
ws.connect("echo.websocket.org")

# Start receiver in background
threading.Thread(target=receiver_thread, args=(ws,), daemon=True).start()

# Send messages
ws.send("Message 1")
ws.send("Message 2")

ws.close()
```

## Response Parsing

### Parse HTTP Response

```python
from netengine.web import ResponseParser

parser = ResponseParser()
http_response = """HTTP/1.1 200 OK\r
Content-Type: application/json\r
Content-Length: 13\r
\r
{"status":"ok"}"""

parsed = parser.parse_http(http_response)
print(parsed["status"])        # "HTTP/1.1 200 OK"
print(parsed["headers"])       # Dict of headers
print(parsed["body"])          # Body content
```

### Parse JSON

```python
json_response = '{"users": [{"id": 1, "name": "John"}]}'
data = parser.parse_json(json_response)
print(data["users"][0]["name"])  # "John"
```

### Extract Headers

```python
headers = parser.extract_headers(http_response)
print(headers["Content-Type"])  # "application/json"
```

### Find Patterns

```python
# Extract all email addresses
response = "Contact us at support@example.com or sales@example.com"
emails = parser.find_pattern(response, r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
print(emails)  # ['support@example.com', 'sales@example.com']

# Extract URLs
urls = parser.find_pattern(response, r'https?://[^\s]+')
```

## Request Building

### Build Custom HTTP Request

```python
from netengine.utils import PacketBuilder

# HTTP GET request
packet = PacketBuilder.http_request_packet(
    method="GET",
    path="/api/users",
    host="api.example.com",
    headers={
        "Authorization": "Bearer token",
        "Accept": "application/json"
    }
)
```

### DNS Query Building

```python
# Build DNS query for A record
dns_packet = PacketBuilder.dns_query_packet("example.com")

# Build DNS query for MX record
dns_packet = PacketBuilder.dns_query_packet("example.com")
```

## Examples

### Example 1: API Testing

```python
from netengine.web import HTTPClient, ResponseParser
from netengine.utils import Logger
import json

logger = Logger()
http = HTTPClient(logger)
parser = ResponseParser(logger)

# Test API endpoint
base_url = "https://jsonplaceholder.typicode.com"

# GET request
response = http.get(f"{base_url}/users/1")
data = parser.parse_json(response)
logger.success(f"User: {data['name']} ({data['email']})")

# POST request
new_post = {"title": "Test", "body": "Content", "userId": 1}
response = http.post(
    f"{base_url}/posts",
    data=json.dumps(new_post).encode(),
    headers={"Content-Type": "application/json"}
)
```

### Example 2: Web Scraping with Parsing

```python
from netengine.web import HTTPClient, ResponseParser

http = HTTPClient()
parser = ResponseParser()

# Get page
response = http.get("https://example.com")

# Extract links
links = parser.find_pattern(response, r'href=["\']([^"\']+)["\']')
print(f"Found {len(links)} links")

# Extract email addresses
emails = parser.find_pattern(response, r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
print(f"Found {len(emails)} emails")
```

### Example 3: Status Code Checker

```python
from netengine.web import HTTPClient

http = HTTPClient()
urls = [
    "https://example.com",
    "https://google.com",
    "https://github.com"
]

for url in urls:
    try:
        response = http.get(url)
        status = response.split('\n')[0]
        print(f"{url}: {status}")
    except Exception as e:
        print(f"{url}: Error - {e}")
```

### Example 4: JSON API Interaction

```python
from netengine.web import HTTPClient, ResponseParser
import json

http = HTTPClient()
parser = ResponseParser()

# Create resource
create_response = http.post(
    "https://api.example.com/resources",
    data=json.dumps({"name": "test"}).encode(),
    headers={"Content-Type": "application/json"}
)

resource = parser.parse_json(create_response)
resource_id = resource["id"]

# Update resource
update_response = http.post(
    f"https://api.example.com/resources/{resource_id}",
    data=json.dumps({"name": "updated"}).encode(),
    headers={"Content-Type": "application/json"}
)

# Parse and display
updated = parser.parse_json(update_response)
print(f"Updated: {updated}")
```

## Advanced Usage

### Concurrent Requests

```python
from netengine.core import ThreadManager
from netengine.web import HTTPClient

def fetch_url(url):
    http = HTTPClient()
    return http.get(url)

urls = [
    "https://api.example.com/1",
    "https://api.example.com/2",
    "https://api.example.com/3",
]

with ThreadManager(max_workers=3) as manager:
    results = manager.map_tasks(fetch_url, urls)
    print(f"Fetched {len(results)} pages")
```

### Error Handling

```python
from netengine.web import HTTPClient
from netengine.utils import Logger

logger = Logger()
http = HTTPClient(logger)

try:
    response = http.get("https://api.example.com/data")
    print("Success!")
except ConnectionError as e:
    logger.error("Connection failed", exc=e)
except TimeoutError as e:
    logger.error("Request timeout", exc=e)
except Exception as e:
    logger.error("Unknown error", exc=e)
```

### Response Caching

```python
from netengine.web import HTTPClient

class CachedHTTPClient(HTTPClient):
    def __init__(self):
        super().__init__()
        self.cache = {}
    
    def get(self, url, headers=None):
        if url in self.cache:
            return self.cache[url]
        
        response = super().get(url, headers)
        self.cache[url] = response
        return response

client = CachedHTTPClient()
result1 = client.get("https://example.com")
result2 = client.get("https://example.com")  # From cache
```

## Security Considerations

### SSL/TLS

NetEngine handles HTTPS automatically:

```python
# Works with self-signed certificates
http = HTTPClient()
response = http.get("https://self-signed.example.com")
```

### Rate Limiting

```python
import time

for page in range(1, 11):
    http.get(f"https://api.example.com/page/{page}")
    time.sleep(1)  # Rate limit: 1 request per second
```

### User-Agent Spoofing

```python
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}
response = http.get("https://example.com", headers=headers)
```

## Common Issues

### SSL Certificate Verification
```
ssl.SSLError: certificate verify failed
```
**Solution**: Use `urllib` with proper certificate handling

### Connection Timeout
```
socket.timeout: _ssl.c:1055: The handshake operation timed out
```
**Solution**: Increase timeout: `http.timeout = 30.0`

### 403 Forbidden
**Solution**: Add proper User-Agent header

### 429 Too Many Requests
**Solution**: Implement rate limiting with delays

## Best Practices

1. Always use proper error handling
2. Set appropriate timeouts
3. Respect rate limits
4. Use proper User-Agent headers
5. Validate responses before parsing
6. Handle SSL/TLS properly
7. Implement retry logic
8. Log all requests
