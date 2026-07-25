from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys
ROOT=find_repository_root(__file__)
paths=[
ROOT/'tests/legacy/strategy_factory/v1/phase_saed_v4_00_program_constitution',
ROOT/'tests/legacy/strategy_factory/v1/phase_saed_v4_01_sovereign_data_foundation',
ROOT/'tests/legacy/strategy_factory/v1/phase_saed_v4_02_context_digital_twin']
raise SystemExit(subprocess.call([sys.executable,'-m','pytest',*[str(x) for x in paths],'-q','--import-mode=importlib']))
