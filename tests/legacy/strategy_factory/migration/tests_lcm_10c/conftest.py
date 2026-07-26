from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
REPO=find_repository_root(__file__)
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
CLOSURE=REPO/'registry/history/lcm/treatment_execution_closures/TREATCLOSE_3EBD9196597715D81966936D37F1DF91'
UPSTREAM=REPO/'registry/history/lcm/treatment_package_migrations/TREATMIG_DCC2F1F7B74985D72A783020843C6B51'
def load(p):return json.loads(p.read_text(encoding="utf-8"))
