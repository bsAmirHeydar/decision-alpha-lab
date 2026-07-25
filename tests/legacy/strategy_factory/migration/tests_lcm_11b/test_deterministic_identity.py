def test_deterministic_identity(migration_root,load):
 d=load(migration_root/"canonical_visualizer_registry.json");ids=[x["visualizer_id"] for x in d["visualizers"]];assert len(ids)==len(set(ids))==128
