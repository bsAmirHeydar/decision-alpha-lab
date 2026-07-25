import sys
from pathlib import Path
PY=Path(__file__).resolve().parents[2]/'python'
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
