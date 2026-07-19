from pathlib import Path
from tools.strategy_factory.lcm.lcm_07.verify import verify_package

def latest(root):return sorted((root/"registry/legacy_context_migration/shared_engines").glob("SHAREDENG_*"))[-1]
def test_reference_package_verifies():
 root=Path(__file__).resolve().parents[4];r=verify_package(latest(root));assert r["passed"];assert r["materialized_engine_count"]==0
def test_handoff_exists_and_blocks_extraction():
 import json
 root=Path(__file__).resolve().parents[4];p=latest(root);h=json.loads((p/"handoff/lcm07_to_lcm08_handoff.json").read_text());assert h["shared_engine_extraction_authorized"] is False;assert h["context_migration_reference_authorized"] is True
