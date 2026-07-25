from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys,os
ROOT=find_repository_root(__file__)
commands=[
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_04/run_saed_v4_04_tests.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_04/validate_saed_v4_04_contracts.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_04/validate_saed_v4_04_obsidian.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_04/validate_saed_v4_04_mql5_static.py']]
for cmd in commands:
 rc=subprocess.call(cmd,cwd=ROOT,env={**os.environ,'PYTHONPATH':str(ROOT/'src/engine/packages')})
 if rc:raise SystemExit(rc)
print('SAED V4-04 full QA passed')
