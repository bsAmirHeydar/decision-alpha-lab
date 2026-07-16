from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
raise SystemExit(subprocess.call([sys.executable,'-m','pytest','-q',str(ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_23_offline_policy_research')],cwd=ROOT))
