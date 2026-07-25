def test_counts(load):
 assert load("quarantine_registry.json")["package_count"]==136
 assert load("observation_registry.json")["record_count"]==272
 assert load("restoration_drill_registry.json")["pass_count"]==136
 assert load("retirement_eligibility_registry.json")["proof_eligible_count"]==136
