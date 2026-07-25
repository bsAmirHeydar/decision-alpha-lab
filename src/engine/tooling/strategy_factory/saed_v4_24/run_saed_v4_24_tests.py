from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess
import sys
ROOT = find_repository_root(__file__)
TESTS = ROOT / 'tests/legacy/strategy_factory/v1/phase_saed_v4_24_conformal_ood_selective_control'
raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', str(TESTS), '-q', '--disable-warnings'], cwd=ROOT).returncode)
