from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from tools.strategy_factory.lcm.lcm_08c.service import build_reference_closure

REPO = find_repository_root(__file__)
ROOT = REPO / "registry/legacy_context_migration/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3"

def test_reference_closure_rebuild_is_deterministic():
    rebuilt = build_reference_closure(REPO)
    stored = json.loads((ROOT / "reports/context_portfolio_closure_report.json").read_text())
    assert rebuilt["closure_id"] == stored["closure_id"]
    assert rebuilt["closure_report"]["closure_report_digest"] == stored["closure_report_digest"]
