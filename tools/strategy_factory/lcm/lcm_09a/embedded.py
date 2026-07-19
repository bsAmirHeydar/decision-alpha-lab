from __future__ import annotations
def validate_candidates(rows:list[dict])->list[str]:
    failures=[]
    for r in rows:
        if r["promoted_to_setup_identity"]: failures.append(r["candidate_id"]+":AUTO_PROMOTED")
        if r["semantic_equivalence_claimed"]: failures.append(r["candidate_id"]+":EQUIVALENCE_CLAIMED")
    return failures
