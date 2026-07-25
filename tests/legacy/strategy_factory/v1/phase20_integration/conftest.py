import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PY=ROOT/"python"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
