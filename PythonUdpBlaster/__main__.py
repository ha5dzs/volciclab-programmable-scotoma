"""CLI entry point.

Works however you invoke it (from the repository root):
  python3 PythonUdpBlaster <ip> <port> <payload> [expect-reply] [-t SECONDS]
  python3 PythonUdpBlaster/__main__.py ...
  python3 -m PythonUdpBlaster ...
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

try:
    from .blaster import main  # running as a package (python3 PythonUdpBlaster / -m)
except ImportError:
    from blaster import main  # running as a plain script (__main__.py directly)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
