def test_parity(migration_root,load):
 d=load(migration_root/"visual_parity_report.json");assert d["semantic_mismatch_count"]==0;assert d["pass_count"]==54;assert d["blocked_count"]==74;assert not d["screenshot_parity_claimed"]
