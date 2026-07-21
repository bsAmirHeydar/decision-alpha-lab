def test_inventory_accounting(migration_root,load):
 d=load(migration_root/"canonical_visualizer_registry.json");assert len(d["visualizers"])==128;assert d["counts"]["reference_cutover_count"]==54;assert d["counts"]["blocked_count"]==74
