def test_visualizer_purity(migration_root,load):
 d=load(migration_root/"canonical_visualizer_registry.json");assert all(x["projection_purity"]=="EVENT_TO_PROJECTION_PURE_FUNCTION" for x in d["visualizers"]);assert not any(x["domain_mutation_allowed"] for x in d["visualizers"])
