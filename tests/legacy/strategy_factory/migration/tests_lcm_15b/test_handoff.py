def test_handoff(load):
 r=load("LCM15B_TO_LCM15C_HANDOFF.json");assert r["future_deletion_approved_count"]==0 and r["deletion_performed"] is False and "LCM15C_EXACT_CONTROLLED_DELETION_REVIEW" in r["allowed_next_actions"]
