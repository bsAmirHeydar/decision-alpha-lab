from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
PYROOT = ROOT / "python"
if str(PYROOT) not in sys.path:
    sys.path.insert(0, str(PYROOT))
