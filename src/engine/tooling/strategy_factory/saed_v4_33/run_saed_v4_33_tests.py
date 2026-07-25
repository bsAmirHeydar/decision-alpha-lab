import os,subprocess,sys
from _common import ROOT,PY_ROOT
env=dict(os.environ);env["PYTHONPATH"]=str(PY_ROOT)+os.pathsep+env.get("PYTHONPATH","")
raise SystemExit(subprocess.call([sys.executable,"-m","pytest","-q",str(ROOT/"tests/legacy/strategy_factory/v1/phase_saed_v4_33_federated_confidential_research")],cwd=ROOT,env=env))
