import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
PYROOT=ROOT/'lab/11_strategy_factory/python'
if str(PYROOT) not in sys.path: sys.path.insert(0,str(PYROOT))
