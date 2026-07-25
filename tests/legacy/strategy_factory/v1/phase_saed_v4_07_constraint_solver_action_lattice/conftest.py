from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
ROOT=find_repository_root(__file__)
PY=ROOT/'src/engine/packages'
if str(PY) not in sys.path:sys.path.insert(0,str(PY))
