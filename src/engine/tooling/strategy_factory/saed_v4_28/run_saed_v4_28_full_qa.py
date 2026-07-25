from tools.repository_paths import find_repository_root
from pathlib import Path
import runpy,sys,time
ROOT=find_repository_root(__file__); TOOL=ROOT/"src/engine/tooling/strategy_factory/saed_v4_28"; PY=ROOT/"src/engine/packages"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
started=time.time(); import pytest
code=pytest.main(["-q",str(ROOT/"tests/legacy/strategy_factory/v1/phase_saed_v4_28_anytime_valid_online_fdr")])
if code: raise SystemExit(code)
for name in ["validate_saed_v4_28_contracts.py","validate_saed_v4_28_status.py","validate_saed_v4_28_obsidian.py","validate_saed_v4_28_mql5_static.py","check_saed_v4_28_boundaries.py","reproduce_saed_v4_28_golden.py"]: runpy.run_path(str(TOOL/name),run_name="__main__")
print(f"V4-28 full QA passed in {time.time()-started:.2f}s")
