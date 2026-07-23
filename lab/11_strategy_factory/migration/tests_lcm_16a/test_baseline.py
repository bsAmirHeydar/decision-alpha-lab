import json

from tools.strategy_factory.lcm.lcm_16a.baseline import build_baseline_amendment
from tools.strategy_factory.lcm.lcm_16a.constants import UPSTREAM_PACKAGE_RELATIVE


def test_baseline_amendment_is_reproducible(root, audit_root):
    expected, rows = build_baseline_amendment(root, root / UPSTREAM_PACKAGE_RELATIVE)
    actual = json.loads((audit_root / "baseline_amendment.json").read_text())
    actual_rows = [json.loads(line) for line in (audit_root / "records/baseline_amendments.jsonl").read_text().splitlines() if line]
    assert actual == expected
    assert actual_rows == rows


def test_amendments_are_exactly_scoped(audit_root):
    rows = [json.loads(line) for line in (audit_root / "records/baseline_amendments.jsonl").read_text().splitlines() if line]
    assert len(rows) == 242
    assert len({row["candidate_path"] for row in rows}) == 242
    assert all(row["candidate_path"].startswith("docs/ai_algorithm_engineering_os/") for row in rows)
    assert all(row["previous_sha256"] != row["amended_sha256"] for row in rows)
    assert not any(row["deletion_approved"] or row["deletion_performed"] for row in rows)
