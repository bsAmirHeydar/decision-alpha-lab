from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
raise SystemExit(subprocess.run([sys.executable,'-m','pytest','-q','lab/11_strategy_factory/tests/phase_saed_v4_12_deep_sequence_state_space_models'],cwd=ROOT).returncode)
