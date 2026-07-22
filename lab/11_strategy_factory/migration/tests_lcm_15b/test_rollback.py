def test_rollback(load):
 r=load("rollback_manifest.json");assert r["rollback_record_count"]==940 and r["documentation_source_restoration_count"]==934 and r["canonical_copy_removal_count"]==6
