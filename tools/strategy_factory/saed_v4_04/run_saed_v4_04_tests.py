from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
cmd=[sys.executable,'-m','pytest','-q',str(ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_04_multimodal_view_platform')]
raise SystemExit(subprocess.call(cmd,cwd=ROOT,env={**__import__('os').environ,'PYTHONPATH':str(ROOT/'lab/11_strategy_factory/python')}))
