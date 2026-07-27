import json
from .conftest import CLOSURE
from src.engine.tooling.strategy_factory.lcm.lcm_10c.fixtures import build_request_case
def test_case_rebuild_is_deterministic():
 p=next((CLOSURE/'dry_run/request_cases').glob('*.json'));case=json.loads(p.read_text());pkg_id=case['package_id'];import pathlib
 repo=CLOSURE.parents[3];up=repo/'registry/history/lcm/treatment_package_migrations/TREATMIG_DCC2F1F7B74985D72A783020843C6B51/canonical_treatment_packages'/f'{pkg_id}.json'
 pkg=json.loads(up.read_text());assert build_request_case(pkg)==case
