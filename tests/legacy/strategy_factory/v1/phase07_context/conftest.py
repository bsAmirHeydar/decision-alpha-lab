from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]/'python'
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
