from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys
ROOT=find_repository_root(__file__)
cmd=[sys.executable,'-m','pytest','-q',str(ROOT/'tests/legacy/strategy_factory/v1/phase_saed_v4_04_multimodal_view_platform')]
raise SystemExit(subprocess.call(cmd,cwd=ROOT,env={**__import__('os').environ,'PYTHONPATH':str(ROOT/'src/engine/packages')}))
