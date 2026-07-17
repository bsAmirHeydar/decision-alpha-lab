from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3]; env=dict(__import__("os").environ); env["PYTHONPATH"]=str(ROOT/"lab/11_strategy_factory/python")+__import__("os").pathsep+env.get("PYTHONPATH","")
raise SystemExit(subprocess.call([sys.executable,"-m","pytest","-q",str(ROOT/"lab/11_strategy_factory/tests/phase_saed_v4_29_hidden_evaluation_air_gap")],cwd=ROOT,env=env))
