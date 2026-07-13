from pathlib import Path
import json
import sys

PHASE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PHASE_ROOT.parents[3]
PYROOT = PHASE_ROOT / "python"
if str(PYROOT) not in sys.path:
    sys.path.insert(0, str(PYROOT))


def load_policy(repo=REPO_ROOT):
    path = repo / "lab/10_infrastructure/EXP0019_faerie_protocol/phase_i00/config/FP_I00_GOVERNANCE_POLICY.v1.json"
    return json.loads(path.read_text(encoding="utf-8"))
