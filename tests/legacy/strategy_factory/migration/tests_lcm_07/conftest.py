from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
ROOT=find_repository_root(__file__)
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
