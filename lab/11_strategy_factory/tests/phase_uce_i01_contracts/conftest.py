from __future__ import annotations
import sys
from pathlib import Path
PYTHON_ROOT=Path(__file__).resolve().parents[2]/"python"
sys.path.insert(0,str(PYTHON_ROOT))
