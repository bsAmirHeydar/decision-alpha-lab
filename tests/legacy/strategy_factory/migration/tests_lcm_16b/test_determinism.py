from src.engine.tooling.strategy_factory.lcm.lcm_16b.canonical import object_digest
from src.engine.tooling.strategy_factory.lcm.lcm_16b.io import load_json


def test_canonical_digest_stable():
    left={"b":2,"a":1}; right={"a":1,"b":2}
    assert object_digest(left) == object_digest(right)


def test_determinism_report(package_root):
    report = load_json(package_root / "reports/determinism_report.json")
    assert report["wall_clock_in_identity"] is False
    assert report["temporary_workspace_in_identity"] is False
    assert report["decision_replay_deterministic"] is True
