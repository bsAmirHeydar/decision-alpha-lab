from pathlib import Path
import json,sys
REPO=Path(__file__).resolve().parents[4]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
CLOSURE=REPO/'registry/legacy_context_migration/treatment_execution_closures/TREATCLOSE_3EBD9196597715D81966936D37F1DF91'
UPSTREAM=REPO/'registry/legacy_context_migration/treatment_package_migrations/TREATMIG_DCC2F1F7B74985D72A783020843C6B51'
def load(p):return json.loads(p.read_text(encoding="utf-8"))
