def test_exact_cutover_accounting(migration_root,load):
 d=load(migration_root/"visual_cutover_manifest.json");states=[x["cutover_state"] for x in d["records"]];assert states.count("REFERENCE_HARNESS_CUTOVER_ACTIVE")==54;assert states.count("BLOCKED_EXPLICIT")==74
