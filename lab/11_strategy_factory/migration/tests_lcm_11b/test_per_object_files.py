def test_per_object_files(migration_root):
 assert len(list((migration_root/"canonical_visualizers").glob("*.json")))==128;assert len(list((migration_root/"golden_fixtures").glob("*.json")))==128;assert len(list((migration_root/"adapters").glob("*.json")))==129
