def test_golden_fixtures(migration_root,load):
 d=load(migration_root/"golden_fixture_registry.json");assert len(d["fixtures"])==128;assert all(x["semantic_fixture"] and not x["screenshot_claimed"] for x in d["fixtures"])
