def test_claim(load):
 for f in ("quarantine_registry.json","observation_registry.json","retirement_eligibility_registry.json"): assert load(f)["claim_ceiling"]=="LCM_14B_REFERENCE_ONLY"
