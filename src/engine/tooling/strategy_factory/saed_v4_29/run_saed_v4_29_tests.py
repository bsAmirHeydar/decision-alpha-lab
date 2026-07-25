from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys
ROOT=find_repository_root(__file__); env=dict(__import__("os").environ); env["PYTHONPATH"]=str(ROOT/"src/engine/packages")+__import__("os").pathsep+env.get("PYTHONPATH","")
raise SystemExit(subprocess.call([sys.executable,"-m","pytest","-q",str(ROOT/"tests/legacy/strategy_factory/v1/phase_saed_v4_29_hidden_evaluation_air_gap")],cwd=ROOT,env=env))
