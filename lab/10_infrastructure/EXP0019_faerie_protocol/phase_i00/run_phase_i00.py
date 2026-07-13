#!/usr/bin/env python3
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PYROOT = HERE / "python"
if str(PYROOT) not in sys.path:
    sys.path.insert(0, str(PYROOT))

from fp_i00_governance.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
