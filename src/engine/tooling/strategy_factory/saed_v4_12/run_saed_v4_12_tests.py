from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys
ROOT=find_repository_root(__file__)
raise SystemExit(subprocess.run([sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_12_deep_sequence_state_space_models'],cwd=ROOT).returncode)
