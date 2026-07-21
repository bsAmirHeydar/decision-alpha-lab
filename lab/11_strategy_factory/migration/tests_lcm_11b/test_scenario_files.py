def test_scenario_files(migration_root):
 assert len(list((migration_root/"isolation_scenarios").glob("*.json")))==512;assert len(list((migration_root/"lifecycle_scenarios").glob("*.json")))==768
