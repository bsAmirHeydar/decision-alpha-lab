from pathlib import Path
import sys
p=Path(__file__).resolve().parents[2]/"python"
if str(p) not in sys.path:sys.path.insert(0,str(p))
