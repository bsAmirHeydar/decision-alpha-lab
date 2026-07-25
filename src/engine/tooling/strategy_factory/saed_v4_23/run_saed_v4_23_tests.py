from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys
ROOT=find_repository_root(__file__)
raise SystemExit(subprocess.call([sys.executable,'-m','pytest','-q',str(ROOT/'tests/legacy/strategy_factory/v1/phase_saed_v4_23_offline_policy_research')],cwd=ROOT))
