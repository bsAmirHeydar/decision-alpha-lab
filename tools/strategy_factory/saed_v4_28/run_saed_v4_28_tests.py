from pathlib import Path
import sys,pytest
ROOT=Path(__file__).resolve().parents[3]; PY=ROOT/"lab/11_strategy_factory/python"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
raise SystemExit(pytest.main(["-q",str(ROOT/"lab/11_strategy_factory/tests/phase_saed_v4_28_anytime_valid_online_fdr")]))
