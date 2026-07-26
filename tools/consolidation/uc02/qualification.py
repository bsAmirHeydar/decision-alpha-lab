"""UC-02 qualification, gate evaluation and handoff issuance."""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from .constants import AUTHORITY_ROOT
from .contracts import validate_contracts
from .generator import deterministic_rebuild, _write_commit_index, _write_hash_ledger
from .guard import run_guard
from .io_utils import read_json, write_json
from .verify import verify_authority_package, verify_static_patch


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _run(command: tuple[str, ...], cwd: Path, timeout: int = 600) -> dict:
    proc = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False, timeout=timeout)
    return {"command": list(command), "exit_code": proc.returncode, "status": "PASS" if proc.returncode == 0 else "FAILED", "output_tail": proc.stdout[-12000:]}


def qualify(repo_root: Path, package_root: Path | None = None) -> dict:
    repo_root = repo_root.resolve()
    package_root = (package_root or repo_root / AUTHORITY_ROOT).resolve()
    checks: dict[str, dict] = {}
    checks["static_patch"] = verify_static_patch(repo_root)
    checks["contracts"] = validate_contracts(repo_root)
    checks["authority_package"] = verify_authority_package(repo_root, package_root)
    checks["guard"] = run_guard(repo_root, require_authority_package=False, receipt_path=package_root / "guard_qualification_receipt.json")
    checks["unit_tests"] = _run((sys.executable, "-m", "pytest", "-q", "tests/consolidation/uc02"), repo_root)
    checks["obsidian_program"] = _run((sys.executable, "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/tools/validate_program_vault.py", "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL"), repo_root)
    checks["repository_policy"] = _run((sys.executable, "tools/engineering/validate_alpha_lab_policy.py", "."), repo_root)
    checks["mql5_static"] = _run((sys.executable, "tools/engineering/check_mql5_compatibility.py", "."), repo_root)
    checks["determinism"] = deterministic_rebuild(repo_root, package_root)
    failed = [name for name, result in checks.items() if result.get("status") != "PASS"]
    receipt = {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": "UC-02",
        "status": "PASS" if not failed else "FAILED",
        "qualified_at_utc": _utc_now(),
        "failed_checks": failed,
        "checks": checks,
        "destructive_authority": False,
        "runtime_authority": False,
        "order_authority": False,
        "broker_authority": False,
        "capital_authority": False,
    }
    write_json(package_root / "qualification_receipt.json", receipt)
    _write_hash_ledger(package_root)
    return receipt


def finalize(repo_root: Path, package_root: Path | None = None) -> dict:
    repo_root = repo_root.resolve()
    package_root = (package_root or repo_root / AUTHORITY_ROOT).resolve()
    coverage = read_json(package_root / "authority_coverage_report.json")
    qualification = read_json(package_root / "qualification_receipt.json")
    guard = read_json(package_root / "guard_qualification_receipt.json")
    contracts = validate_contracts(repo_root)

    gates = {
        "uc01_handoff_accepted": False,
        "artifact_authority_coverage_complete": coverage.get("artifact_coverage_ratio") == 1.0,
        "unresolved_authority_zero": coverage.get("unresolved_count") == 0,
        "capability_inventory_present": int(coverage.get("capability_count", 0)) > 0,
        "package_destinations_complete": int(coverage.get("package_count", 0)) > 0,
        "system_disposition_complete": int(coverage.get("system_count", 0)) == 10,
        "contracts_valid": contracts.get("status") == "PASS",
        "guards_qualified": guard.get("status") == "PASS",
        "qualification_passed": qualification.get("status") == "PASS",
        "destructive_authority_disabled": True,
    }
    uc01_decision_path = repo_root / "registry/consolidation/uc01/baselines/UC01_BASELINE_V1/stage_exit_decision.json"
    if uc01_decision_path.is_file():
        uc01 = read_json(uc01_decision_path)
        gates["uc01_handoff_accepted"] = uc01.get("status") == "ACCEPTED" and uc01.get("uc02_authorized") is True

    status = "ACCEPTED" if all(gates.values()) else "BLOCKED"
    decision = {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": "UC-02",
        "status": status,
        "uc03_authorized": status == "ACCEPTED",
        "evaluated_at_utc": _utc_now(),
        "gates": gates,
        "blocking_gates": [name for name, passed in gates.items() if not passed],
        "destructive_authority": False,
        "runtime_authority": False,
        "order_authority": False,
        "broker_authority": False,
        "capital_authority": False,
    }
    write_json(package_root / "stage_exit_decision.json", decision)

    manifest = read_json(package_root / "authority_manifest.json")
    handoff = {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": "UC-02",
        "status": "ISSUED" if status == "ACCEPTED" else "WITHHELD",
        "authority_package_id": manifest["authority_package_id"],
        "authority_package_digest": manifest["artifact_authority_digest_sha256"],
        "uc03_authorized": status == "ACCEPTED",
        "canonical_topology": "contracts/platform/canonical_topology.yaml",
        "capability_ownership": "contracts/platform/capability_ownership.yaml",
        "system_disposition": "contracts/platform/system_disposition.yaml",
        "repository_authority_ledger": f"{package_root.relative_to(repo_root).as_posix()}/repository_authority_ledger.jsonl.gz",
        "wave_portfolio": f"{package_root.relative_to(repo_root).as_posix()}/wave_portfolio.json",
        "uc03_constraints": [
            "Move before semantic refactor.",
            "Use git mv where identity is preserved.",
            "Do not delete or merge logic without a preservation certificate.",
            "Do not weaken differential root or parallel-engine guards.",
            "No destructive authority is granted by this handoff.",
        ],
        "destructive_authority": False,
    }
    write_json(package_root / "uc03_handoff.json", handoff)
    _write_commit_index(repo_root, package_root)
    _write_hash_ledger(package_root)
    return decision
