def test_blockers(load):
 r=load("deletion_blocker_registry.json");assert r["deletion_blocked_candidate_count"]==2168 and r["external_unknown_blocker_count"]==2168
