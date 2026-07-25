from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys
ROOT=find_repository_root(__file__);cmd=[sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_14_foundation_model_adapters'];raise SystemExit(subprocess.run(cmd,cwd=ROOT).returncode)
