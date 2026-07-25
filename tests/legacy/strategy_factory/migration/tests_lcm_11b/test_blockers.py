def test_blockers(migration_root,load):
 d=load(migration_root/"blockers/blocker_resolution_registry.json");assert d["open"];assert all(x["state"] in {"CARRIED_BLOCKING","OPEN_BLOCKING"} for x in d["open"])
