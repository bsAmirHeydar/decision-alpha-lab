from tools.repository_paths import find_repository_root
from pathlib import Path
import sys,pytest
ROOT=find_repository_root(__file__); PY=ROOT/"src/engine/packages"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
raise SystemExit(pytest.main(["-q",str(ROOT/"tests/legacy/strategy_factory/v1/phase_saed_v4_28_anytime_valid_online_fdr")]))
