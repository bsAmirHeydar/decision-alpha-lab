"""Build the UC-02 authority-freeze package from the accepted UC-01 baseline."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import jsonschema
import yaml

from .classification import classify_artifact, classify_symbol
from tools.consolidation.uc01.classification import (
    classify_authorship, classify_category, classify_lifecycle, critical_domains,
    criticality, detect_language, owner_domain, probable_production_source,
)
from .constants import (
    AUTHORITY_DOMAINS,
    AUTHORITY_PACKAGE_NAME,
    AUTHORITY_ROOT,
    DYNAMIC_OUTPUTS,
    PLANNING_DISPOSITIONS,
    RELEASE_ROOT,
    SCHEMA_ROOT,
    STATIC_CONTRACT_FILES,
    STATIC_POLICY_FILES,
    STAGE_ID,
    UC01_BASELINE_ROOT,
    VERSION,
)
from .contracts import validate_contracts
from .io_utils import iter_jsonl_gz, read_json, root_digest, sha256_file, write_json, write_jsonl_gz


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _require_uc01(repo_root: Path, *, allow_reference: bool = False) -> tuple[Path, dict]:
    baseline = repo_root / UC01_BASELINE_ROOT
    if not baseline.is_dir():
        raise RuntimeError(f"UC-01 baseline missing: {baseline}")
    decision_path = baseline / "stage_exit_decision.json"
    if not decision_path.is_file():
        if allow_reference:
            return baseline, {"status": "REFERENCE_ONLY", "uc02_authorized": False}
        raise RuntimeError("UC-01 stage exit decision is missing")
    decision = read_json(decision_path)
    if not allow_reference and (decision.get("status") != "ACCEPTED" or decision.get("uc02_authorized") is not True):
        raise RuntimeError("UC-01 has not accepted and authorized UC-02")
    return baseline, decision



def _current_nonbaseline_rows(repo_root: Path, baseline_paths: set[str]) -> list[dict]:
    rows: list[dict] = []
    excluded_prefix = AUTHORITY_ROOT.as_posix().rstrip("/") + "/"
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        parts = path.relative_to(repo_root).parts
        if any(part in {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"} for part in parts) or rel.endswith(".pyc"):
            continue
        if rel.startswith(excluded_prefix):
            continue
        if rel in baseline_paths:
            continue
        category = classify_category(rel)
        rows.append({
            "path": rel,
            "sha256": sha256_file(path),
            "size": path.stat().st_size,
            "object_type": "file",
            "mode": oct(path.stat().st_mode & 0o777),
            "suffix": path.suffix.lower(),
            "language": detect_language(path),
            "category": category,
            "lifecycle": classify_lifecycle(rel),
            "authorship": classify_authorship(rel),
            "owner_domain": owner_domain(rel),
            "critical_domains": critical_domains(rel),
            "criticality": criticality(rel, category),
            "production_source_candidate": probable_production_source(rel),
            "git_status": "post_uc01_controlled_addition",
            "lfs_pointer": False,
            "disposition": "UNASSESSED_UNTIL_UC02",
        })
    return rows

def _top_level(path: str) -> str:
    parts = PurePosixPath(path).parts
    return parts[0] if parts else path


def _package_key(path: str) -> str:
    parts = PurePosixPath(path).parts
    if not parts:
        return path
    if parts[0] == "lab" and len(parts) >= 4 and parts[1] == "11_strategy_factory" and parts[2] == "python":
        return "/".join(parts[:4])
    if parts[0] == "tools" and len(parts) >= 3:
        return "/".join(parts[:3])
    if parts[0] in {"src", "contexts", "adapters", "mql5", "tests", "docs", "registry", "product_lab", "products"}:
        return "/".join(parts[: min(len(parts), 3)])
    return parts[0]


def _documentation_class(row: dict, artifact: dict) -> str:
    path = artifact["path"].lower()
    if artifact["planning_disposition"] == "EXTERNALIZE" or artifact["canonical_owner"] in {"release_history", "historical_archive"}:
        return "HISTORICAL_RELEASE"
    if path.startswith("docs/") and row.get("frontmatter_present") and row.get("status") in {"approved", "active", "canonical"}:
        return "NORMATIVE_AUTHORED"
    if "/contexts/" in path or artifact["system_id"] in {"RTHP", "NDS", "EXPERIMENTS"}:
        return "CONTEXT_AUTHORED"
    if "generated" in path or artifact.get("source_category") == "generated_artifact":
        return "GENERATED_PROJECTION"
    return "NORMATIVE_CANDIDATE_REVIEW"


def _load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"YAML root is not an object: {path}")
    return value


def _validate_row_schema(repo_root: Path, rows: list[dict]) -> list[str]:
    schema = json.loads((repo_root / SCHEMA_ROOT / "authority_ledger_row.schema.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    required = ("path", "canonical_owner", "canonical_target", "planning_disposition", "migration_action", "migration_wave")
    for index, row in enumerate(rows):
        missing = [field for field in required if not isinstance(row.get(field), str) or not row.get(field)]
        if missing:
            errors.append(f"authority row {index} missing required fields: {missing}")
            if len(errors) >= 20:
                return errors
        if index < 100:
            try:
                jsonschema.validate(row, schema)
            except Exception as exc:
                errors.append(f"authority row {index} invalid: {exc}")
                if len(errors) >= 20:
                    return errors
    return errors


def _write_hash_ledger(root: Path) -> None:
    ledger_path = root / "authority_output_hashes.sha256"
    names = [name for name in DYNAMIC_OUTPUTS if name not in {"authority_output_hashes.sha256", "UC02_COMMIT_FILE_INDEX.txt"}]
    lines = []
    for name in names:
        path = root / name
        if path.is_file():
            lines.append(f"{sha256_file(path)}  {name}")
    ledger_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _static_paths(repo_root: Path) -> list[str]:
    index = repo_root / RELEASE_ROOT / "UC02_PATCH_FILE_INDEX.txt"
    return [line.strip().replace("\\", "/") for line in index.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_commit_index(repo_root: Path, package_root: Path) -> None:
    static_paths = _static_paths(repo_root)
    dynamic_paths = [f"{AUTHORITY_ROOT.as_posix()}/{name}" for name in DYNAMIC_OUTPUTS]
    paths = sorted(set(static_paths + dynamic_paths))
    (package_root / "UC02_COMMIT_FILE_INDEX.txt").write_text("\n".join(paths) + "\n", encoding="utf-8", newline="\n")


def build_authority_package(repo_root: Path, package_root: Path | None = None, *, allow_reference: bool = False) -> dict:
    repo_root = repo_root.resolve()
    package_root = (package_root or repo_root / AUTHORITY_ROOT).resolve()
    baseline, uc01_decision = _require_uc01(repo_root, allow_reference=allow_reference)
    if package_root.exists() and any(package_root.iterdir()):
        raise RuntimeError(f"authority package root is not empty: {package_root}")
    package_root.mkdir(parents=True, exist_ok=True)

    contract_result = validate_contracts(repo_root)
    if contract_result["status"] != "PASS":
        raise RuntimeError(f"UC-02 contracts failed validation: {contract_result['errors']}")

    artifact_source = list(iter_jsonl_gz(baseline / "artifact_inventory.jsonl.gz"))
    baseline_paths = {str(row["path"]) for row in artifact_source}
    artifact_source.extend(_current_nonbaseline_rows(repo_root, baseline_paths))
    artifact_source.sort(key=lambda row: str(row["path"]))
    artifact_rows = [classify_artifact(row) for row in artifact_source]
    artifact_rows.sort(key=lambda row: row["path"])

    unresolved: list[dict] = []
    for row in artifact_rows:
        if row.get("canonical_owner") not in AUTHORITY_DOMAINS:
            unresolved.append({"kind": "invalid_owner", "path": row.get("path"), "value": row.get("canonical_owner")})
        if row.get("planning_disposition") not in PLANNING_DISPOSITIONS:
            unresolved.append({"kind": "invalid_disposition", "path": row.get("path"), "value": row.get("planning_disposition")})
        if not row.get("canonical_target") or not row.get("migration_wave") or not row.get("migration_action"):
            unresolved.append({"kind": "missing_authority_field", "path": row.get("path")})
        if any(row.get(flag) is not False for flag in ("destructive_authority", "runtime_authority", "order_authority", "broker_authority", "capital_authority")):
            unresolved.append({"kind": "authority_escalation", "path": row.get("path")})
    unresolved.extend({"kind": "schema", "detail": error} for error in _validate_row_schema(repo_root, artifact_rows))

    write_jsonl_gz(package_root / "repository_authority_ledger.jsonl.gz", artifact_rows)

    package_groups: dict[str, list[dict]] = defaultdict(list)
    for row in artifact_rows:
        package_groups[_package_key(row["path"])].append(row)
    package_rows = []
    for package, rows in sorted(package_groups.items()):
        owners = Counter(row["canonical_owner"] for row in rows)
        targets = Counter(row["canonical_target"] for row in rows)
        dispositions = Counter(row["planning_disposition"] for row in rows)
        systems = Counter(row["system_id"] for row in rows)
        package_rows.append({
            "package": package,
            "artifact_count": len(rows),
            "canonical_owner": owners.most_common(1)[0][0],
            "owner_distribution": dict(sorted(owners.items())),
            "primary_target": targets.most_common(1)[0][0],
            "target_distribution": dict(sorted(targets.items())),
            "primary_disposition": dispositions.most_common(1)[0][0],
            "disposition_distribution": dict(sorted(dispositions.items())),
            "primary_system": systems.most_common(1)[0][0],
            "system_distribution": dict(sorted(systems.items())),
            "destructive_authority": False,
        })
    write_jsonl_gz(package_root / "package_authority_ledger.jsonl.gz", package_rows)

    capability_rows: list[dict] = []
    for row in iter_jsonl_gz(baseline / "python_symbol_inventory.jsonl.gz"):
        capability_rows.append(classify_symbol(str(row["path"]), str(row.get("qualified_name") or row.get("name")), str(row.get("kind", "symbol")), "python"))
    for row in iter_jsonl_gz(baseline / "mql5_symbol_inventory.jsonl.gz"):
        capability_rows.append(classify_symbol(str(row["path"]), str(row.get("name")), str(row.get("kind", "symbol")), "mql5"))
    capability_rows.sort(key=lambda row: (row["language"], row["path"], row["symbol"], row["symbol_kind"]))
    write_jsonl_gz(package_root / "capability_authority_ledger.jsonl.gz", capability_rows)

    artifact_by_path = {row["path"]: row for row in artifact_rows}
    documentation_rows = []
    for row in iter_jsonl_gz(baseline / "documentation_inventory.jsonl.gz"):
        artifact = artifact_by_path.get(str(row["path"]))
        if artifact is None:
            unresolved.append({"kind": "documentation_without_artifact", "path": row.get("path")})
            continue
        documentation_rows.append({
            "path": row["path"],
            "note_id": row.get("note_id"),
            "title": row.get("title"),
            "document_class": _documentation_class(row, artifact),
            "canonical_owner": "documentation",
            "canonical_target": artifact["canonical_target"],
            "planning_disposition": artifact["planning_disposition"],
            "successor_required": artifact["planning_disposition"] in {"MERGE", "MOVE", "EXTERNALIZE", "DELETE"},
            "destructive_authority": False,
        })
    documentation_rows.sort(key=lambda row: row["path"])
    write_jsonl_gz(package_root / "documentation_authority_ledger.jsonl.gz", documentation_rows)

    system_contract = _load_yaml(repo_root / "contracts/platform/system_disposition.yaml")
    system_counts = Counter(row["system_id"] for row in artifact_rows)
    system_rows = []
    for system_id, contract in sorted(system_contract["systems"].items()):
        system_rows.append({
            "system_id": system_id,
            "observed_artifact_count": system_counts.get(system_id, 0),
            "decision": contract["decision"],
            "canonical_destinations": contract["canonical_destinations"],
            "special_rule": contract["special_rule"],
            "parallel_platform_authority_after_uc04": False,
            "destructive_authority": False,
        })
    write_jsonl_gz(package_root / "system_disposition_ledger.jsonl.gz", system_rows)

    root_files = sorted(row["path"] for row in artifact_source if "/" not in str(row["path"]))
    top_level_dirs = sorted({_top_level(str(row["path"])) for row in artifact_source if "/" in str(row["path"])})
    write_json(package_root / "root_grandfather_baseline.json", {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": STAGE_ID,
        "source": UC01_BASELINE_ROOT.as_posix(),
        "root_file_count": len(root_files),
        "root_files": root_files,
        "top_level_directories": top_level_dirs,
        "debt_is_grandfathered_not_compliant": True,
        "destructive_authority": False,
    })
    write_json(package_root / "package_grandfather_baseline.json", {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": STAGE_ID,
        "packages": [row["package"] for row in package_rows],
        "package_count": len(package_rows),
        "new_parallel_engines_forbidden": True,
        "destructive_authority": False,
    })

    wave_counts = Counter(row["migration_wave"] for row in artifact_rows)
    disposition_counts = Counter(row["planning_disposition"] for row in artifact_rows)
    owner_counts = Counter(row["canonical_owner"] for row in artifact_rows)
    target_counts = Counter(row["canonical_target"] for row in artifact_rows)
    review_count = sum(1 for row in artifact_rows if row["review_required"])
    wave_portfolio = {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": STAGE_ID,
        "waves": [{"wave_id": wave, "artifact_count": count, "destructive_authority": False} for wave, count in sorted(wave_counts.items())],
        "dispositions": dict(sorted(disposition_counts.items())),
        "owners": dict(sorted(owner_counts.items())),
        "top_targets": dict(target_counts.most_common(100)),
        "review_required_count": review_count,
        "review_required_is_uc03_planning_not_unknown_authority": True,
        "destructive_authority": False,
    }
    write_json(package_root / "wave_portfolio.json", wave_portfolio)

    baseline_manifest = read_json(baseline / "baseline_manifest.json")
    authority_digest = root_digest(artifact_rows, key_fields=("path",))
    capability_digest = root_digest(capability_rows, key_fields=("language", "path", "symbol", "symbol_kind"))
    coverage = {
        "artifact_count": len(artifact_rows),
        "artifact_authority_count": len(artifact_rows) - len([item for item in unresolved if item.get("path")]),
        "artifact_coverage_ratio": 1.0 if not artifact_rows else (len(artifact_rows) - len([item for item in unresolved if item.get("path")])) / len(artifact_rows),
        "package_count": len(package_rows),
        "capability_count": len(capability_rows),
        "documentation_count": len(documentation_rows),
        "system_count": len(system_rows),
        "unresolved_count": len(unresolved),
        "review_required_count": review_count,
        "owner_count": len(owner_counts),
        "disposition_count": len(disposition_counts),
    }
    write_json(package_root / "authority_coverage_report.json", coverage)
    write_jsonl_gz(package_root / "unresolved_authority_items.jsonl.gz", sorted(unresolved, key=lambda row: json.dumps(row, sort_keys=True)))

    manifest = {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": STAGE_ID,
        "version": VERSION,
        "authority_package_id": f"UC02AUTH_{authority_digest[:32].upper()}",
        "package_name": AUTHORITY_PACKAGE_NAME,
        "generated_at_utc": _utc_now(),
        "reference_mode": allow_reference,
        "uc01_status": uc01_decision.get("status"),
        "uc01_baseline_id": baseline_manifest.get("baseline_id"),
        "uc01_root_digest": baseline_manifest.get("repository_root_digest_sha256"),
        "artifact_authority_digest_sha256": authority_digest,
        "capability_authority_digest_sha256": capability_digest,
        "contract_digests": contract_result["digests"],
        "coverage": coverage,
        "immutable_after_acceptance": True,
        "destructive_authority": False,
        "runtime_authority": False,
        "order_authority": False,
        "broker_authority": False,
        "capital_authority": False,
    }
    write_json(package_root / "authority_manifest.json", manifest)

    pending = {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": STAGE_ID,
        "status": "PENDING",
        "uc03_authorized": False,
        "gates": {},
        "destructive_authority": False,
    }
    write_json(package_root / "stage_exit_decision.json", pending)
    write_json(package_root / "uc03_handoff.json", {
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": STAGE_ID,
        "status": "WITHHELD",
        "authority_package_id": manifest["authority_package_id"],
        "authority_package_digest": authority_digest,
        "reason": "UC-02 qualification and finalization have not completed.",
        "destructive_authority": False,
    })
    write_json(package_root / "guard_qualification_receipt.json", {"status": "PENDING", "destructive_authority": False})
    write_json(package_root / "qualification_receipt.json", {"status": "PENDING", "destructive_authority": False})
    _write_hash_ledger(package_root)
    _write_commit_index(repo_root, package_root)
    _write_hash_ledger(package_root)
    return {"status": "PASS" if not unresolved else "FAILED", "package_root": str(package_root), **coverage, "authority_package_id": manifest["authority_package_id"]}


def deterministic_rebuild(repo_root: Path, canonical_root: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="uc02-rebuild-") as temp:
        rebuilt = Path(temp) / AUTHORITY_PACKAGE_NAME
        result = build_authority_package(repo_root, rebuilt, allow_reference=True)
        ignored = {"generated_at_utc", "uc01_status", "reference_mode"}
        canonical_manifest = read_json(canonical_root / "authority_manifest.json")
        rebuilt_manifest = read_json(rebuilt / "authority_manifest.json")
        for key in ignored:
            canonical_manifest.pop(key, None)
            rebuilt_manifest.pop(key, None)
        errors = []
        if canonical_manifest != rebuilt_manifest:
            errors.append("authority manifest differs under deterministic rebuild")
        for name in (
            "repository_authority_ledger.jsonl.gz", "package_authority_ledger.jsonl.gz",
            "capability_authority_ledger.jsonl.gz", "documentation_authority_ledger.jsonl.gz",
            "system_disposition_ledger.jsonl.gz", "root_grandfather_baseline.json",
            "package_grandfather_baseline.json", "wave_portfolio.json", "authority_coverage_report.json",
            "unresolved_authority_items.jsonl.gz",
        ):
            if sha256_file(canonical_root / name) != sha256_file(rebuilt / name):
                errors.append(f"deterministic rebuild mismatch: {name}")
        return {"status": "PASS" if not errors else "FAILED", "errors": errors, "reference_build_status": result["status"]}
