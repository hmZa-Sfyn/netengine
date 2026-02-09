"""Example: Using extensions."""

from netengine.core import NetworkEngine, Config

config = Config(verbose=True)
engine = NetworkEngine(config)

# Load port scanner extension
try:
    engine.load_extension("scanner", "./examples/extensions/port_scanner.py")
    result = engine.execute_extension("scanner", "localhost", [80, 443, 8080])
    print(f"Open ports: {result}")
except Exception as e:
    print(f"Error: {e}")

engine.shutdown()
