from pathlib import Path
import runpy, sys, time
ROOT=Path(__file__).resolve().parents[3]; TOOL=ROOT/"tools/strategy_factory/saed_v4_27"; PY=ROOT/"lab/11_strategy_factory/python"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
started=time.time(); import pytest
code=pytest.main(["-q",str(ROOT/"lab/11_strategy_factory/tests/phase_saed_v4_27_complete_search_exposure_ledger")])
if code: raise SystemExit(code)
for name in ["validate_saed_v4_27_contracts.py","validate_saed_v4_27_status.py","validate_saed_v4_27_obsidian.py","validate_saed_v4_27_mql5_static.py","check_saed_v4_27_boundaries.py","reproduce_saed_v4_27_golden.py"]: runpy.run_path(str(TOOL/name),run_name="__main__")
print(f"V4-27 full QA passed in {time.time()-started:.2f}s")
