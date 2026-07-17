from pathlib import Path
import os,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]; env=dict(os.environ); py=str(ROOT/"lab/11_strategy_factory/python"); env["PYTHONPATH"]=py+(os.pathsep+env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
raise SystemExit(subprocess.run([sys.executable,"-m","pytest","-q",str(ROOT/"lab/11_strategy_factory/tests/phase_saed_v4_26_mechanistic_interpretability")],cwd=ROOT,env=env).returncode)
