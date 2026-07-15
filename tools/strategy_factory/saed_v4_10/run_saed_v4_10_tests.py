from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
raise SystemExit(subprocess.call([sys.executable,'-m','pytest','-q','lab/11_strategy_factory/tests/phase_saed_v4_10_baseline_manual_program'],cwd=ROOT))
