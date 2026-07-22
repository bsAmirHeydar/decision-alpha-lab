def test_claim(load):
 for f in ("deletion_candidate_ledger.json","reference_proof_registry.json","deletion_approval_registry.json"): assert load(f)["claim_ceiling"]=="LCM_15A_REFERENCE_ONLY"
