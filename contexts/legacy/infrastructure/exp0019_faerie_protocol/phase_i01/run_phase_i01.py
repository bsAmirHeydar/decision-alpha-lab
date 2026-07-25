from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'python'))
from fp_i01_compatibility.cli import main
if __name__=='__main__':raise SystemExit(main([str(HERE.parents[3]),'--json']))
