from pathlib import Path
import subprocess,sys,os
ROOT=Path(__file__).resolve().parents[3]
commands=[
 [sys.executable,'tools/strategy_factory/saed_v4_04/run_saed_v4_04_tests.py'],
 [sys.executable,'tools/strategy_factory/saed_v4_04/validate_saed_v4_04_contracts.py'],
 [sys.executable,'tools/strategy_factory/saed_v4_04/validate_saed_v4_04_obsidian.py'],
 [sys.executable,'tools/strategy_factory/saed_v4_04/validate_saed_v4_04_mql5_static.py']]
for cmd in commands:
 rc=subprocess.call(cmd,cwd=ROOT,env={**os.environ,'PYTHONPATH':str(ROOT/'lab/11_strategy_factory/python')})
 if rc:raise SystemExit(rc)
print('SAED V4-04 full QA passed')
