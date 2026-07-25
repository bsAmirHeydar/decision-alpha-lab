from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from tools.strategy_factory.lcm.lcm_08c.canonical import file_digest

REPO = find_repository_root(__file__)
ROOT = REPO / "registry/legacy_context_migration/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3"

def rows(name):
    return [json.loads(x) for x in (ROOT / name).read_text().splitlines() if x.strip()]

def test_all_source_locks_match_repository_bytes():
    for row in rows("registries/source_lock_ledger.jsonl"):
        assert row["verified"]
        packet = json.loads((ROOT / "context_migration_packets" / f"{row['identity_id']}.json").read_text())
        assert file_digest(REPO / packet["source_artifact_path"]) == row["expected_sha256"]

def test_locator_registry_is_casefold_collision_free():
    locators = rows("registries/canonical_locator_registry.jsonl")
    paths = [x["target_path_proposal"].casefold() for x in locators]
    assert len(paths) == len(set(paths)) == 321
    assert not any(x["locator_collision"] for x in locators)
