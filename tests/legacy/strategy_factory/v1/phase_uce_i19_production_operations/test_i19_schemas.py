from tools.repository_paths import find_repository_root
import json
from pathlib import Path

ROOT=find_repository_root(__file__)


def test_all_i19_schemas_are_closed_and_identified():
    paths=sorted((ROOT/'schemas/legacy/strategy_factory/v3').glob('operations_*.schema.json'))
    assert len(paths)>=24
    for path in paths:
        value=json.loads(path.read_text())
        assert value['$schema'].endswith('2020-12/schema')
        assert value['type']=='object'
        assert value['additionalProperties'] is False
        assert value['$id'].startswith('https://decision-alpha-lab.local/schemas/v3/')


def test_reference_artifacts_remain_blocked():
    base=ROOT/'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i19'
    for name in ('reference_blocked_operations_bundle.json','limitations.json'):
        value=json.loads((base/name).read_text())
        assert value['activation_allowed'] is False


def test_test_vectors_are_json_objects():
    base=ROOT/'tests/fixtures/legacy/strategy_factory/v3/uce_i19'
    paths=list(base.glob('*.json')); assert len(paths)>=6
    assert all(isinstance(json.loads(path.read_text()),dict) for path in paths)
