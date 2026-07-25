from pathlib import Path

from tools.consolidation.uc02.generator import deterministic_rebuild
from tools.consolidation.uc02.io_utils import iter_jsonl_gz, read_json
from tools.consolidation.uc02.verify import verify_authority_package


def test_reference_package_has_complete_artifact_coverage(repo_root: Path, reference_authority: Path) -> None:
    coverage = read_json(reference_authority / "authority_coverage_report.json")
    assert coverage["artifact_coverage_ratio"] == 1.0
    assert coverage["unresolved_count"] == 0
    assert coverage["artifact_count"] > 52000


def test_every_artifact_has_one_owner(reference_authority: Path) -> None:
    rows = list(iter_jsonl_gz(reference_authority / "repository_authority_ledger.jsonl.gz"))
    assert rows
    assert all(isinstance(row["canonical_owner"], str) and row["canonical_owner"] for row in rows)
    assert len({row["path"] for row in rows}) == len(rows)


def test_capabilities_cover_python_and_mql5(reference_authority: Path) -> None:
    rows = list(iter_jsonl_gz(reference_authority / "capability_authority_ledger.jsonl.gz"))
    languages = {row["language"] for row in rows}
    assert languages == {"python", "mql5"}
    assert len(rows) > 39000


def test_no_dynamic_authority_escalation(reference_authority: Path) -> None:
    for row in iter_jsonl_gz(reference_authority / "repository_authority_ledger.jsonl.gz"):
        assert row["destructive_authority"] is False
        assert row["runtime_authority"] is False
        assert row["order_authority"] is False
        assert row["broker_authority"] is False
        assert row["capital_authority"] is False


def test_system_ledger_has_ten_decisions(reference_authority: Path) -> None:
    rows = list(iter_jsonl_gz(reference_authority / "system_disposition_ledger.jsonl.gz"))
    assert len(rows) == 10
    assert all(row["parallel_platform_authority_after_uc04"] is False for row in rows)


def test_reference_package_verifies(repo_root: Path, reference_authority: Path) -> None:
    result = verify_authority_package(repo_root, reference_authority)
    assert result["status"] == "PASS", result


def test_authority_rebuild_is_deterministic(repo_root: Path, reference_authority: Path) -> None:
    result = deterministic_rebuild(repo_root, reference_authority)
    assert result["status"] == "PASS", result
