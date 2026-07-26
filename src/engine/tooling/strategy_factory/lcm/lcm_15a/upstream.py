from __future__ import annotations
from pathlib import Path
from .io import load_json
EXPECTED="sha256:beb66a4bb6792692608c4223763f7f88198e62d63a51b217436e1b456ab02cb8"
def verify_upstream(repo_root:Path)->dict:
    roots=list((repo_root/"registry/history/lcm/quarantine_observations").iterdir())
    if len(roots)!=1: raise ValueError("LCM14B quarantine root is not unique")
    handoff=load_json(roots[0]/"LCM14B_TO_LCM15A_HANDOFF.json")
    if handoff.get("handoff_digest")!=EXPECTED: raise ValueError("LCM14B handoff digest mismatch")
    return handoff
