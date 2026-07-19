from pathlib import Path
import json

REPO = Path(__file__).resolve().parents[4]
ROOT = REPO / "registry/legacy_context_migration/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3"

def rows(name):
    return [json.loads(x) for x in (ROOT / name).read_text().splitlines() if x.strip()]

def test_every_context_has_exactly_one_packet_and_disposition():
    packages = rows("registries/context_package_registry.jsonl")
    packets = list((ROOT / "context_migration_packets").glob("*.json"))
    assert len(packages) == len(packets) == 321
    assert len({x["identity_id"] for x in packages}) == 321
    assert sum(x["final_disposition"] == "MIGRATED_CUTOVER_READY" for x in packages) == 1
    assert sum(x["final_disposition"] == "BLOCKED" for x in packages) == 320

def test_every_blocked_context_has_blocker_record():
    packages = rows("registries/context_package_registry.jsonl")
    blockers = rows("registries/context_blocker_registry.jsonl")
    blocked_ids = {x["identity_id"] for x in packages if x["final_disposition"] == "BLOCKED"}
    assert blocked_ids == {x["identity_id"] for x in blockers}
    assert all(x["blocker_count"] == len(x["blocker_reasons"]) > 0 for x in blockers)
