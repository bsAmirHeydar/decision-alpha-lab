def test_reference_adapter_scope(migration_root,load):
 d=load(migration_root/"adapters/consumer_adapter_registry.json");assert len(d["adapters"])==128;assert all(x["enabled_scope"]=="LCM11B_REFERENCE_HARNESS_ONLY" for x in d["adapters"]);assert not any(x["source_mutation_allowed"] for x in d["adapters"])
