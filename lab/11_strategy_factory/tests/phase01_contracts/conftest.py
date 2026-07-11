from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
PY = ROOT / "python"
if str(PY) not in sys.path:
    sys.path.insert(0, str(PY))
