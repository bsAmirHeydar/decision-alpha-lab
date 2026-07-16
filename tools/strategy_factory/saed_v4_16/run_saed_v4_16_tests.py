from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
r=subprocess.run([sys.executable,'-m','pytest','-q','lab/11_strategy_factory/tests/phase_saed_v4_16_distributional_survival_tail'],cwd=ROOT)
raise SystemExit(r.returncode)
