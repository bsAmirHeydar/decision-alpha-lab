def test_cutover(migration_root,load):
 d=load(migration_root/"visual_cutover_manifest.json");assert d["cutover_mode"]=="REFERENCE_HARNESS_ONLY";assert d["production_source_mutation_count"]==0;assert d["legacy_source_delete_count"]==0;assert d["exact_reversible_path_list"]
