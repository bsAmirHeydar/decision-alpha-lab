def test_style_separation(migration_root,load):
 d=load(migration_root/"style_profile_registry.json");assert len(d["profiles"])==128;assert not any(x["style_affects_semantics"] for x in d["profiles"])
