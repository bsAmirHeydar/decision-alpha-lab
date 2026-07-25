from tools.repository_paths import find_repository_root
from pathlib import Path
import os,subprocess,sys
ROOT=find_repository_root(__file__); env=dict(os.environ); py=str(ROOT/"src/engine/packages"); env["PYTHONPATH"]=py+(os.pathsep+env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
raise SystemExit(subprocess.run([sys.executable,"-m","pytest","-q",str(ROOT/"tests/legacy/strategy_factory/v1/phase_saed_v4_26_mechanistic_interpretability")],cwd=ROOT,env=env).returncode)
