from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3];cmd=[sys.executable,'-m','pytest','-q','lab/11_strategy_factory/tests/phase_saed_v4_19_neurosymbolic_setup_reasoning']
r=subprocess.run(cmd,cwd=ROOT);raise SystemExit(r.returncode)
