def test_handoff(load):
 h=load("LCM14B_TO_LCM15A_HANDOFF.json")
 assert h["handoff_type"]=="LCM14B_TO_LCM15A"
 assert h["proof_eligible_count"]==136 and h["deletion_approved_count"]==0
 assert "DELETE_ANY_LEGACY_ARTIFACT" in h["forbidden_actions"]
