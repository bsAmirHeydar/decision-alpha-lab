from tools.repository_paths import find_repository_root
import sys
from pathlib import Path
ROOT=find_repository_root(__file__)
PYROOT=ROOT/'src/engine/packages'
if str(PYROOT) not in sys.path: sys.path.insert(0,str(PYROOT))
