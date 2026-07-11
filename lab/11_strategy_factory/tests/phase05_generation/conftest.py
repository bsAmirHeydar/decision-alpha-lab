import sys
from pathlib import Path
P=Path(__file__).resolve().parents[2]/'python'
if str(P) not in sys.path:sys.path.insert(0,str(P))
