def test_source_binding(migration_root,load):
 d=load(migration_root/"canonical_visualizer_registry.json");assert all(x["source_event_type"] for x in d["visualizers"])
