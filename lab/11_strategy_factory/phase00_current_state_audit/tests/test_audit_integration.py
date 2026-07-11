from __future__ import annotations

import json
from pathlib import Path

import pytest

from sf_phase00.audit import AuditConfig, RepositoryAuditor, run_audit


def _minimal_repo(tmp_path: Path) -> Path:
    (tmp_path / "lab" / "core").mkdir(parents=True)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    (tmp_path / "lab" / "core" / "engine.py").write_text(
        "class Engine:\n    def run(self):\n        return 1\n", encoding="utf-8"
    )
    return tmp_path


def test_missing_repository_root_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Not a Decision Alpha Lab root"):
        RepositoryAuditor(tmp_path, AuditConfig(run_pytest=False)).run()


def test_full_audit_writes_required_artifacts(tmp_path: Path) -> None:
    repo = _minimal_repo(tmp_path / "repo")
    output = tmp_path / "out"
    result = run_audit(repo, output, AuditConfig(run_pytest=False))
    required = {
        "current_state_report.md",
        "duplicate_engine_matrix.csv",
        "migration_risk_register.json",
        "repository_inventory.json",
        "module_classification.csv",
        "execution_authority_scan.csv",
        "phase00_qa_report.json",
    }
    assert required.issubset({path.name for path in output.iterdir()})
    assert result.summary["phase_gate_status"] == "ACCEPTED_WITH_DEFERRED_REMEDIATIONS"
    qa = json.loads((output / "phase00_qa_report.json").read_text(encoding="utf-8"))
    assert qa["passed"] is True


def test_duplicate_or_replayed_files_have_stable_hashes(tmp_path: Path) -> None:
    repo = _minimal_repo(tmp_path / "repo")
    duplicate = repo / "lab" / "core" / "engine_copy.py"
    duplicate.write_bytes((repo / "lab" / "core" / "engine.py").read_bytes())
    result = RepositoryAuditor(repo, AuditConfig(run_pytest=False)).run()
    hashes = [record.sha256 for record in result.files if record.path.endswith(".py")]
    assert len(hashes) == 2
    assert len(set(hashes)) == 1
