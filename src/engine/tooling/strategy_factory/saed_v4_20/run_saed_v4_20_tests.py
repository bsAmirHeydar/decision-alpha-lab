from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys
ROOT=find_repository_root(__file__)
cmd=[sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_20_decision_focused_treatment_selection']
r=subprocess.run(cmd,cwd=ROOT);raise SystemExit(r.returncode)
