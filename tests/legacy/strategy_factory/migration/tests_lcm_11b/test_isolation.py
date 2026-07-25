def test_isolation(migration_root,load):
 d=load(migration_root/"multi_chart_test_report.json");assert d["scenario_count"]==512;assert d["canonical_collision_count"]==0;assert d["pass_count"]==216
