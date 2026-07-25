def test_contradictions_are_not_silently_harmonized(load):
    reg=load("documentation_contradiction_registry.json")
    assert reg["silent_harmonization_count"]==0
    assert all(c["decision_status"]=="BLOCKED_OWNER_DECISION" and c["silent_harmonization_performed"] is False for c in reg["contradictions"])
