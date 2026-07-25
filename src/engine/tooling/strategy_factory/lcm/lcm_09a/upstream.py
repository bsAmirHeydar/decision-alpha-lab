from __future__ import annotations
from pathlib import Path
from .io import load_json,load_jsonl
IDENTITY_ROOT="registry/legacy_context_migration/identities/IDENTITY_A3F7E93C3F5154CB2616F01F5235F748"
CHAR_ROOT="registry/legacy_context_migration/characterizations/CHARACTERIZATION_55F06219A834717D91B7111A481DF3D3"
CLOSURE_ROOT="registry/legacy_context_migration/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3"
def load_upstream(repo:Path)->dict:
    identities=load_jsonl(repo/IDENTITY_ROOT/"identities/canonical_identity_candidates.jsonl")
    setups=sorted([x for x in identities if x["identity_kind"]=="SETUP"],key=lambda x:x["identity_id"])
    handoff=load_json(repo/CLOSURE_ROOT/"handoff/lcm08c_to_lcm09a_handoff.json")
    return {"setups":setups,"handoff":handoff}
