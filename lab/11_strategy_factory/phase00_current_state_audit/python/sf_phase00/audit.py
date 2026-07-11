from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .authority import scan_execution_authority
from .classifier import classify_modules
from .contracts import extract_python_contracts
from .duplicates import detect_duplicate_capabilities
from .models import AuditResult
from .reporting import write_artifacts
from .risks import build_risk_register
from .scanner import scan_files
from .testing import collect_test_baseline


@dataclass(frozen=True)
class AuditConfig:
    run_pytest: bool = True


def _git_commit(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"


class RepositoryAuditor:
    def __init__(self, repo_root: Path, config: AuditConfig | None = None):
        self.repo_root = repo_root.resolve()
        self.config = config or AuditConfig()

    def validate_root(self) -> None:
        required = [self.repo_root / "lab", self.repo_root / "docs"]
        missing = [path.as_posix() for path in required if not path.exists()]
        if missing:
            raise ValueError(f"Not a Decision Alpha Lab root; missing: {missing}")

    def run(self) -> AuditResult:
        self.validate_root()
        files = scan_files(self.repo_root)
        modules = classify_modules(self.repo_root)
        authority = scan_execution_authority(self.repo_root)
        contracts = extract_python_contracts(self.repo_root)
        duplicates = detect_duplicate_capabilities(self.repo_root)
        test_baseline = collect_test_baseline(self.repo_root, run_pytest=self.config.run_pytest)
        risks = build_risk_register(
            self.repo_root,
            authority,
            bool(test_baseline.get("pytest", {}).get("passed")),
        )
        generated_at = datetime.now(timezone.utc).isoformat()
        summary: dict[str, Any] = {
            "phase": "PHASE_00",
            "phase_gate_status": "ACCEPTED_WITH_DEFERRED_REMEDIATIONS" if not authority else "BLOCKED",
            "file_count": len(files),
            "empty_file_count": sum(item.is_empty for item in files),
            "module_count": len(modules),
            "contract_count": len(contracts),
            "duplicate_capability_count": len(duplicates),
            "authority_finding_count": len(authority),
            "risk_count": len(risks),
            "pytest_passed": bool(test_baseline.get("pytest", {}).get("passed")),
        }
        return AuditResult(
            repo_root=self.repo_root,
            generated_at_utc=generated_at,
            git_commit=_git_commit(self.repo_root),
            files=files,
            modules=modules,
            authority_findings=authority,
            contracts=contracts,
            duplicates=duplicates,
            risks=risks,
            test_baseline=test_baseline,
            summary=summary,
        )


def run_audit(repo_root: Path, output_dir: Path, config: AuditConfig | None = None) -> AuditResult:
    result = RepositoryAuditor(repo_root, config).run()
    write_artifacts(result, output_dir)
    return result
