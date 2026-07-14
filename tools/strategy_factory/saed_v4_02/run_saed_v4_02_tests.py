from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
paths=[
ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_00_program_constitution',
ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_01_sovereign_data_foundation',
ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_02_context_digital_twin']
raise SystemExit(subprocess.call([sys.executable,'-m','pytest',*[str(x) for x in paths],'-q','--import-mode=importlib']))
