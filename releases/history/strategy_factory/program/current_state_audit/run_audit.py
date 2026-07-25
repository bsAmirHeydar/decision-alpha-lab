from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent / "python"
sys.path.insert(0, str(PACKAGE_ROOT))

from sf_phase00.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
