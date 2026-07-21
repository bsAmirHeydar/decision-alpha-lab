def test_acceptance(migration_root,load):
 d=load(migration_root/"reports/acceptance_report.json");assert d["passed"];assert all(d["gates"].values())
