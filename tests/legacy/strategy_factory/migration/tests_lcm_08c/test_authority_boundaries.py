from tools.repository_paths import find_repository_root
from pathlib import Path
import json

REPO = find_repository_root(__file__)
ROOT = REPO / "registry/legacy_context_migration/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3"

def test_handoff_denies_cutover_and_authority():
    h = json.loads((ROOT / "handoff/lcm08c_to_lcm09a_handoff.json").read_text())
    for key in ("consumer_cutover_allowed","source_move_allowed","source_delete_allowed","runtime_authority_created","live_order_authority_created","capital_authority_created"):
        assert h[key] is False
    assert "TREAT_BLOCKED_CONTEXT_AS_CANONICAL" in h["forbidden_actions"]

def test_packets_deny_source_and_execution_authority():
    for p in (ROOT / "context_migration_packets").glob("*.json"):
        row = json.loads(p.read_text())
        for key in ("consumer_cutover_performed","source_move_performed","source_delete_performed","runtime_authority_created","live_order_authority_created","capital_authority_created"):
            assert row[key] is False
