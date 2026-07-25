def test_output_manifest(migration_root,load):
 d=load(migration_root/"output_manifest.json");assert d["file_count"]>1500;assert d["total_size_bytes"]>500000
