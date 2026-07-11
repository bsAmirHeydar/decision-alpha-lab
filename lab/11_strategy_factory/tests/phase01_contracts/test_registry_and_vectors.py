import json
from pathlib import Path
from strategy_factory_contracts import default_registry

def test_registry_unique_and_complete():
    registry=default_registry()
    assert len(registry.schemas)==5
    assert len(registry.as_dict())==5

def test_cross_language_vectors_present():
    root=Path(__file__).resolve().parents[2]
    payload=json.loads((root/"test_vectors/v1/cross_language_vectors.json").read_text())
    assert payload["hash_algorithm"]=="FNV1A64_UTF16LE"
    assert payload["event"]["expected_id"].startswith("evt_")
