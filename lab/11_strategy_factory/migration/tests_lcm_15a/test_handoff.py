def test_handoff(load):
 h=load("LCM15A_TO_LCM15B_HANDOFF.json");assert h["approved_future_deletion_count"]==0 and "DELETE_ANY_CANDIDATE_DURING_LCM15B" in h["forbidden_actions"]
