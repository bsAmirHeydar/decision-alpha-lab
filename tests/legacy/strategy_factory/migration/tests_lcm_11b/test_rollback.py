def test_rollback(migration_root,load):
 d=load(migration_root/"visual_rollback_manifest.json");assert d["legacy_source_retained"];assert not d["production_source_restoration_required"];assert len(d["cutover_records"])==128
