from pathlib import Path
from .io import load_json
EXPECTED='sha256:65f12eae61307a4b008bb593e8f5d09466e3839db03e549809bcfeb1584018bd'
def verify_upstream(repo_root:Path):
 p=repo_root/"registry/legacy_context_migration/deletion_candidate_proofs/DELCAND_DBF53BE0F1838F171906F990E05930D6/LCM15A_TO_LCM15B_HANDOFF.json"
 obj=load_json(p)
 if obj.get("handoff_digest")!=EXPECTED or obj.get("validation_status")!="PASS":raise ValueError("LCM-15A handoff mismatch")
 return obj
