def test_hostile_review(migration_root,load):
 d=load(migration_root/"reports/hostile_review.json");assert d["aggregate_success_cannot_override_blocker"];assert all(x["result"]=="PASS" for x in d["tests"])
