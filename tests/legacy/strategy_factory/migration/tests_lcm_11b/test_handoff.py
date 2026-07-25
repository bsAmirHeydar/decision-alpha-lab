def test_handoff(migration_root,load):
 d=load(migration_root/"LCM11B_TO_LCM12A_HANDOFF.json");assert d["handoff_type"]=="LCM11B_TO_LCM12A";assert not d["runtime_authority_created"];assert not d["live_order_authority_created"];assert not d["capital_authority_created"];assert "MAP_CANONICAL_DOCUMENTATION_AUTHORITY" in d["allowed_next_actions"]
