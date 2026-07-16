from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[3]
TESTS = ROOT / 'lab/11_strategy_factory/tests/phase_saed_v4_24_conformal_ood_selective_control'
raise SystemExit(subprocess.run([sys.executable, '-m', 'pytest', str(TESTS), '-q', '--disable-warnings'], cwd=ROOT).returncode)
