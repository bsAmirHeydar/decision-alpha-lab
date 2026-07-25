def test_release_index(load):
 r=load("release_registry_index.json");assert r["release_artifact_count"]==6 and r["historical_lookup_preserved_count"]==6
