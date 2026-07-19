from pathlib import Path
from tools.strategy_factory.lcm.lcm_08c.verify import verify_package

REPO = Path(__file__).resolve().parents[4]
ROOT = REPO / "registry/legacy_context_migration/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3"

def test_reference_package_verifies():
    out = verify_package(ROOT)
    assert out["passed"]
    assert out["portfolio_record_count"] == 321
    assert out["migrated_count"] == 1
    assert out["blocked_count"] == 320
