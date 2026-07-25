from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
ROOT=find_repository_root(__file__)
PKG=ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i01/python'
if str(PKG) not in sys.path:sys.path.insert(0,str(PKG))
