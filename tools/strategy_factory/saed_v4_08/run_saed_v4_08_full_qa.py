from pathlib import Path
import os,runpy,sys
ROOT=Path(__file__).resolve().parents[3];PY=ROOT/'lab/11_strategy_factory/python';sys.path.insert(0,str(PY));os.environ['PYTHONPATH']=str(PY)
for rel in ('tools/strategy_factory/saed_v4_08/reproduce_saed_v4_08_golden.py','tools/strategy_factory/saed_v4_08/validate_saed_v4_08_contracts.py','tools/strategy_factory/saed_v4_08/check_saed_v4_08_boundaries.py','tools/strategy_factory/saed_v4_08/validate_saed_v4_08_obsidian.py','tools/strategy_factory/saed_v4_08/validate_saed_v4_08_mql5_static.py'):
 try:runpy.run_path(str(ROOT/rel),run_name='__main__')
 except SystemExit as e:
  if e.code not in (None,0):raise
import pytest
code=pytest.main(['-q',str(ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_08_executable_path_outcome_cube')])
if code:raise SystemExit(code)
print('SAED V4-08 full QA passed')
