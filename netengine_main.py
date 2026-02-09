#!/usr/bin/env python3
"""NetEngine - Main entry point."""

import sys
from netengine.cli import CLI


def main():
    """Main entry point."""
    cli = CLI()
    try:
        cli.run(sys.argv[1:])
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
