from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys
ROOT=find_repository_root(__file__)
r=subprocess.run([sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_18_causal_treatment_policy_value'],cwd=ROOT)
raise SystemExit(r.returncode)
