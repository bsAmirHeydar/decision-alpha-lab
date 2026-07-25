from tools.repository_paths import find_repository_root
import sys
from pathlib import Path
ROOT=find_repository_root(__file__)
PY=ROOT/'src/engine/packages'
if str(PY) not in sys.path:sys.path.insert(0,str(PY))
