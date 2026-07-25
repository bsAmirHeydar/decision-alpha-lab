def test_restart_backfill(migration_root,load):
 d=load(migration_root/"restart_backfill_test_report.json");assert d["scenario_count"]==768;assert d["domain_state_mutation_count"]==0;assert d["pass_count"]==324
