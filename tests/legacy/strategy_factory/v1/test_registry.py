from strategy_factory.registry import JsonRegistry, RegistryEntry


def test_registry_round_trip(tmp_path):
    path = tmp_path / "registry.json"
    registry = JsonRegistry(path)
    registry.add(RegistryEntry("m1", "model", "1", "candidate", "model.bin", "abc", {}))
    registry.save()
    loaded = JsonRegistry(path)
    assert loaded.get("m1").artifact_hash == "abc"
