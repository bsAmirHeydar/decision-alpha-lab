"""UC-01 complete preservation and resumable baseline capture."""
from __future__ import annotations

import hashlib
import re
import subprocess
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .archive import create_source_archive, recovery_drill, root_digest_from_rows
from .behavior import build_critical_logic_inventory
from .classification import (
    classify_authorship,
    classify_category,
    classify_lifecycle,
    critical_domains,
    criticality,
    detect_language,
    owner_domain,
    probable_production_source,
)
from .constants import BASELINE_RELATIVE_ROOT, BASELINE_STABILIZATION_REPAIR_PATHS, EXCLUDED_DIRECTORY_NAMES, IMPLEMENTATION_VERSION, RELEASE_RELATIVE_ROOT, STAGE_ID
from .document_scan import scan_documents, scan_path_references, scan_schemas
from .environment import capture_environment
from .git_utils import create_git_preservation, git_available, git_metadata, git_status_map, lfs_inventory, list_repository_files, run_command
from .io_utils import is_probable_lfs_pointer, iter_jsonl_gz, path_mode, read_json, sha256_file, write_json, write_jsonl_gz
from .mql5_scan import scan_mql5
from .python_scan import scan_python
from .qualification import run_qualification

_SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
_CAPTURE_STEPS = ("artifacts", "python", "mql5", "documents", "references", "assemble")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _state_path(root: Path) -> Path:
    return root / "capture_state.json"


def _load_state(root: Path) -> dict:
    path = _state_path(root)
    if path.is_file():
        return read_json(path)
    return {"stage_id": STAGE_ID, "steps": {}, "created_at": _utc_now()}


def _record_step(root: Path, step: str, status: str, details: dict) -> None:
    state = _load_state(root)
    state["steps"][step] = {"status": status, "recorded_at": _utc_now(), **details}
    state["updated_at"] = _utc_now()
    write_json(_state_path(root), state)
    _write_hash_ledger(root)


def _included_paths(repo_root: Path) -> tuple[list[str], str]:
    paths, source = list_repository_files(repo_root)
    baseline_prefix = BASELINE_RELATIVE_ROOT.as_posix().rstrip("/") + "/"
    filtered = []
    for path in paths:
        parts = Path(path).parts
        if path.startswith(baseline_prefix):
            continue
        if any(part in EXCLUDED_DIRECTORY_NAMES for part in parts):
            continue
        if path.endswith(".pyc"):
            continue
        filtered.append(path)
    return sorted(set(filtered)), source


def _hash_artifacts(repo_root: Path, paths: Iterable[str]) -> tuple[list[dict], list[dict]]:
    status_map = git_status_map(repo_root)
    rows: list[dict] = []
    unresolved: list[dict] = []
    for rel in paths:
        path = repo_root / rel
        try:
            is_link = path.is_symlink()
            if is_link:
                payload = path.readlink().as_posix().encode("utf-8")
                digest = hashlib.sha256(payload).hexdigest()
                size = len(payload)
                object_type = "symlink"
            else:
                digest = sha256_file(path)
                size = path.stat().st_size
                object_type = "file"
            category = classify_category(rel)
            rows.append({
                "path": rel,
                "sha256": digest,
                "size": size,
                "object_type": object_type,
                "mode": path_mode(path),
                "suffix": path.suffix.lower(),
                "language": detect_language(path),
                "category": category,
                "lifecycle": classify_lifecycle(rel),
                "authorship": classify_authorship(rel),
                "owner_domain": owner_domain(rel),
                "critical_domains": critical_domains(rel),
                "criticality": criticality(rel, category),
                "production_source_candidate": probable_production_source(rel),
                "git_status": status_map.get(rel, "tracked_or_clean"),
                "lfs_pointer": is_probable_lfs_pointer(path),
                "disposition": "UNASSESSED_UNTIL_UC02",
            })
        except Exception as exc:
            unresolved.append({"kind": "artifact_hash_failure", "path": rel, "severity": "BLOCKING", "error": f"{type(exc).__name__}: {exc}"})
    return sorted(rows, key=lambda x: x["path"]), sorted(unresolved, key=lambda x: (x["kind"], x["path"]))


def _secret_scan(repo_root: Path, artifact_rows: Iterable[dict]) -> list[dict]:
    findings: list[dict] = []
    allowed_suffixes = {".py", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".ps1", ".sh", ".env"}
    for row in artifact_rows:
        if row["suffix"] not in allowed_suffixes or row["size"] > 2 * 1024 * 1024:
            continue
        path = repo_root / row["path"]
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern_index, pattern in enumerate(_SECRET_PATTERNS, 1):
            match = pattern.search(text)
            if match:
                lowered_path = row["path"].lower()
                detector_or_fixture = (
                    "/tests/" in f"/{lowered_path}"
                    or lowered_path.startswith("tests/")
                    or Path(lowered_path).name.startswith("test_")
                    or "scanner" in lowered_path
                    or "security.py" in lowered_path
                    or "validation.py" in lowered_path
                    or Path(lowered_path).name.startswith("validate_")
                )
                findings.append({
                    "kind": "probable_secret_material",
                    "path": row["path"],
                    "line": text.count("\n", 0, match.start()) + 1,
                    "pattern_id": f"SECRET_PATTERN_{pattern_index:02d}",
                    "severity": "RECORDED" if detector_or_fixture else "BLOCKING",
                    "classification": "detector_or_fixture_literal" if detector_or_fixture else "requires_security_review",
                    "content_copied": False,
                })
                break
    return findings


def _summary(rows: list[dict]) -> dict:
    def count(field: str) -> dict:
        return dict(sorted(Counter(str(row.get(field)) for row in rows).items()))
    return {
        "file_count": len(rows),
        "total_bytes": sum(row["size"] for row in rows),
        "category_counts": count("category"),
        "language_counts": count("language"),
        "lifecycle_counts": count("lifecycle"),
        "owner_domain_counts": count("owner_domain"),
        "criticality_counts": count("criticality"),
        "top_level_counts": dict(sorted(Counter(row["path"].split("/", 1)[0] for row in rows).items())),
        "lfs_pointer_count": sum(1 for row in rows if row["lfs_pointer"]),
        "production_source_candidate_count": sum(1 for row in rows if row["production_source_candidate"]),
    }


def _write_hash_ledger(root: Path) -> None:
    ledger = root / "baseline_output_hashes.sha256"
    lines = [f"{sha256_file(path)}  {path.name}" for path in sorted(p for p in root.iterdir() if p.is_file() and p.name != ledger.name)]
    ledger.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def capture_artifacts(repo_root: Path, root: Path) -> dict:
    started = time.time()
    paths, enumeration_source = _included_paths(repo_root)
    rows, issues = _hash_artifacts(repo_root, paths)
    issues.extend(_secret_scan(repo_root, rows))
    lfs_rows, lfs_status = lfs_inventory(repo_root)
    for row in lfs_rows:
        if row["materialization_marker"] != "*" or not row["exists"]:
            issues.append({"kind": "lfs_not_materialized", "path": row["path"], "severity": "BLOCKING", "details": row})
    write_jsonl_gz(root / "artifact_inventory.jsonl.gz", rows)
    summary = _summary(rows)
    write_json(root / "artifact_inventory_summary.json", summary)
    write_jsonl_gz(root / "large_object_inventory.jsonl.gz", [
        {"path": row["path"], "size": row["size"], "sha256": row["sha256"], "category": row["category"], "lfs_pointer": row["lfs_pointer"]}
        for row in rows if row["size"] >= 5 * 1024 * 1024
    ])
    write_jsonl_gz(root / "git_lfs_inventory.jsonl.gz", lfs_rows)
    write_jsonl_gz(root / "artifact_scan_issues.jsonl.gz", sorted(issues, key=lambda x: (x.get("severity", ""), x.get("kind", ""), x.get("path", ""))))
    write_json(root / "environment_manifest.json", capture_environment(repo_root))
    digest = root_digest_from_rows(rows)
    write_json(root / "repository_snapshot.json", {
        "captured_at": _utc_now(),
        "enumeration_source": enumeration_source,
        "root_digest_sha256": digest,
        "file_count": len(rows),
        "total_bytes": summary["total_bytes"],
        "git": git_metadata(repo_root),
        "lfs": lfs_status,
        "excluded_prefixes": [BASELINE_RELATIVE_ROOT.as_posix()],
        "destructive_authority": False,
    })
    details = {"file_count": len(rows), "root_digest_sha256": digest, "duration_seconds": round(time.time() - started, 3)}
    _record_step(root, "artifacts", "PASS" if not any(x.get("severity") == "BLOCKING" and x.get("kind") == "artifact_hash_failure" for x in issues) else "FAILED", details)
    return details


def capture_python_surface(repo_root: Path, root: Path) -> dict:
    started = time.time()
    artifacts = list(iter_jsonl_gz(root / "artifact_inventory.jsonl.gz"))
    paths = [row["path"] for row in artifacts if row["language"] == "python"]
    result = scan_python(repo_root, paths)
    write_jsonl_gz(root / "python_symbol_inventory.jsonl.gz", result["symbols"])
    write_jsonl_gz(root / "python_import_graph.jsonl.gz", result["imports"])
    write_jsonl_gz(root / "python_parse_issues.jsonl.gz", result["issues"])
    write_jsonl_gz(root / "test_inventory.jsonl.gz", result["tests"])
    details = {"source_count": len(paths), "symbol_count": len(result["symbols"]), "import_count": len(result["imports"]), "issue_count": len(result["issues"]), "test_symbol_count": len(result["tests"]), "duration_seconds": round(time.time() - started, 3)}
    _record_step(root, "python", "PASS", details)
    return details


def capture_mql5_surface(repo_root: Path, root: Path) -> dict:
    started = time.time()
    artifacts = list(iter_jsonl_gz(root / "artifact_inventory.jsonl.gz"))
    paths = [row["path"] for row in artifacts if row["language"] == "mql5"]
    result = scan_mql5(repo_root, paths)
    write_jsonl_gz(root / "mql5_symbol_inventory.jsonl.gz", result["symbols"])
    write_jsonl_gz(root / "mql5_include_graph.jsonl.gz", result["includes"])
    write_jsonl_gz(root / "mql5_authority_surface.jsonl.gz", result["authority"])
    write_jsonl_gz(root / "mql5_scan_issues.jsonl.gz", result["issues"])
    details = {"source_count": len(paths), "symbol_count": len(result["symbols"]), "include_count": len(result["includes"]), "authority_surface_count": len(result["authority"]), "issue_count": len(result["issues"]), "duration_seconds": round(time.time() - started, 3)}
    _record_step(root, "mql5", "PASS" if not result["issues"] else "BLOCKED", details)
    return details


def capture_documents_and_schemas(repo_root: Path, root: Path) -> dict:
    started = time.time()
    artifacts = list(iter_jsonl_gz(root / "artifact_inventory.jsonl.gz"))
    doc_paths = [row["path"] for row in artifacts if row["category"] == "documentation"]
    result = scan_documents(repo_root, doc_paths)
    schema_paths = [row["path"] for row in artifacts if row["suffix"] in {".json", ".yaml", ".yml", ".xsd", ".proto"}]
    schemas, schema_issues = scan_schemas(repo_root, schema_paths)
    write_jsonl_gz(root / "documentation_inventory.jsonl.gz", result["documents"])
    write_jsonl_gz(root / "documentation_link_graph.jsonl.gz", result["links"])
    write_jsonl_gz(root / "documentation_id_collisions.jsonl.gz", result["collisions"])
    write_jsonl_gz(root / "documentation_scan_issues.jsonl.gz", result["issues"])
    write_jsonl_gz(root / "schema_inventory.jsonl.gz", schemas)
    write_jsonl_gz(root / "schema_scan_issues.jsonl.gz", schema_issues)
    details = {"document_count": len(result["documents"]), "link_count": len(result["links"]), "id_collision_count": len(result["collisions"]), "schema_count": len(schemas), "issue_count": len(result["issues"]) + len(schema_issues), "duration_seconds": round(time.time() - started, 3)}
    _record_step(root, "documents", "PASS", details)
    return details


def capture_path_references(repo_root: Path, root: Path) -> dict:
    started = time.time()
    artifacts = list(iter_jsonl_gz(root / "artifact_inventory.jsonl.gz"))
    executable_suffixes = {".py", ".pyi", ".mq5", ".mqh", ".ps1", ".psm1", ".sh", ".bat", ".cmd", ".toml", ".ini", ".cfg"}
    structured_suffixes = {".json", ".yaml", ".yml"}
    paths = []
    for row in artifacts:
        suffix = row["suffix"]
        rel = row["path"].lower()
        if suffix in executable_suffixes:
            paths.append(row["path"])
            continue
        if suffix in structured_suffixes and (
            rel.startswith(".github/")
            or rel.startswith("configs/")
            or rel.startswith("policies/")
            or "/configs/" in rel
            or "/policies/" in rel
            or rel.endswith("pyproject.toml")
        ):
            paths.append(row["path"])
    refs, issues = scan_path_references(repo_root, paths)
    write_jsonl_gz(root / "path_reference_graph.jsonl.gz", refs)
    write_jsonl_gz(root / "path_reference_scan_issues.jsonl.gz", issues)
    details = {"scanned_text_file_count": len(paths), "reference_count": len(refs), "issue_count": len(issues), "duration_seconds": round(time.time() - started, 3)}
    _record_step(root, "references", "PASS", details)
    return details


def _consumer_inventory(python_imports: list[dict], mql_includes: list[dict], doc_links: list[dict], path_refs: list[dict]) -> list[dict]:
    rows: list[dict] = []
    rows.extend({"consumer_path": x["source_path"], "target": x.get("resolved_path") or x.get("target_module"), "kind": "python_import", "resolved": bool(x.get("resolved_path")), "line": x.get("line")} for x in python_imports)
    rows.extend({"consumer_path": x["source_path"], "target": x["target_include"], "kind": "mql5_include", "resolved": None, "line": x.get("line")} for x in mql_includes)
    rows.extend({"consumer_path": x["source_path"], "target": x["target"], "kind": x["kind"], "resolved": None, "line": None} for x in doc_links)
    rows.extend({"consumer_path": x["source_path"], "target": x["target_path_text"], "kind": "path_reference", "resolved": x["target_exists"], "line": x.get("line")} for x in path_refs)
    return sorted(rows, key=lambda x: (x["consumer_path"], x["kind"], str(x["target"]), x.get("line") or 0))



def _baseline_stabilization_receipt(repo_root: Path) -> dict:
    release_manifest_path = repo_root / RELEASE_RELATIVE_ROOT / "UC01_PATCH_MANIFEST.json"
    if not release_manifest_path.is_file():
        return {"status": "FAILED", "reason": "uc01_patch_manifest_missing"}
    manifest = read_json(release_manifest_path)
    declared_paths = tuple(manifest.get("modified_paths", []))
    expected_paths = tuple(BASELINE_STABILIZATION_REPAIR_PATHS)
    original_hashes = manifest.get("repair_original_sha256", {})
    patched_hashes = manifest.get("repair_patched_sha256", {})
    path_set_valid = set(declared_paths) == set(expected_paths)
    rows: list[dict] = []
    git_is_available = git_available(repo_root)
    for rel in expected_paths:
        current_path = repo_root / rel
        current_hash = sha256_file(current_path) if current_path.is_file() else None
        original_hash = None
        original_status = "BLOCKED_GIT_UNAVAILABLE"
        if git_is_available:
            try:
                proc = subprocess.run(
                    ["git", "show", f"HEAD:{rel}"],
                    cwd=repo_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                if proc.returncode == 0:
                    original_hash = hashlib.sha256(proc.stdout).hexdigest()
                    original_status = "PASS" if original_hash == original_hashes.get(rel) else "FAILED"
                else:
                    original_status = "FAILED_GIT_SHOW"
            except OSError as exc:
                original_status = f"FAILED_{type(exc).__name__}"
        current_status = "PASS" if current_hash == patched_hashes.get(rel) else "FAILED"
        rows.append({
            "path": rel,
            "expected_original_sha256": original_hashes.get(rel),
            "observed_head_sha256": original_hash,
            "original_verification_status": original_status,
            "expected_patched_sha256": patched_hashes.get(rel),
            "observed_current_sha256": current_hash,
            "patched_verification_status": current_status,
            "transformation_class": "mechanical_newline_literal_syntax_restoration",
        })
    deleted_paths: list[str] = []
    if git_is_available:
        result = run_command(("git", "diff", "--name-only", "--diff-filter=D"), repo_root, timeout=30)
        deleted_paths = sorted({line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()})
    current_pass = all(row["patched_verification_status"] == "PASS" for row in rows)
    original_pass = git_is_available and all(row["original_verification_status"] == "PASS" for row in rows)
    status = "PASS" if path_set_valid and current_pass and original_pass and not deleted_paths else "BLOCKED"
    if not path_set_valid or not current_pass or deleted_paths:
        status = "FAILED"
    return {
        "status": status,
        "repair_count": len(rows),
        "declared_path_set_matches_constant": path_set_valid,
        "git_head_pre_repair_verification_available": git_is_available,
        "all_original_hashes_verified": original_pass,
        "all_patched_hashes_verified": current_pass,
        "deleted_paths_detected": deleted_paths,
        "moved_paths_authorized": False,
        "source_mutation_performed_by_capture": False,
        "baseline_stabilization_repairs": rows,
        "repair_class": "mechanical_newline_literal_syntax_restoration",
        "semantic_change_claimed": False,
        "pre_repair_state_preservation_required": True,
        "baseline_output_root_excluded_from_snapshot": BASELINE_RELATIVE_ROOT.as_posix(),
    }

def assemble_baseline(repo_root: Path, root: Path) -> dict:
    started = time.time()
    artifacts = list(iter_jsonl_gz(root / "artifact_inventory.jsonl.gz"))
    py_symbols = list(iter_jsonl_gz(root / "python_symbol_inventory.jsonl.gz"))
    py_imports = list(iter_jsonl_gz(root / "python_import_graph.jsonl.gz"))
    py_issues = list(iter_jsonl_gz(root / "python_parse_issues.jsonl.gz"))
    tests = list(iter_jsonl_gz(root / "test_inventory.jsonl.gz"))
    mql_symbols = list(iter_jsonl_gz(root / "mql5_symbol_inventory.jsonl.gz"))
    mql_includes = list(iter_jsonl_gz(root / "mql5_include_graph.jsonl.gz"))
    mql_issues = list(iter_jsonl_gz(root / "mql5_scan_issues.jsonl.gz"))
    docs = list(iter_jsonl_gz(root / "documentation_inventory.jsonl.gz"))
    doc_links = list(iter_jsonl_gz(root / "documentation_link_graph.jsonl.gz"))
    doc_collisions = list(iter_jsonl_gz(root / "documentation_id_collisions.jsonl.gz"))
    doc_issues = list(iter_jsonl_gz(root / "documentation_scan_issues.jsonl.gz"))
    schemas = list(iter_jsonl_gz(root / "schema_inventory.jsonl.gz"))
    schema_issues = list(iter_jsonl_gz(root / "schema_scan_issues.jsonl.gz"))
    path_refs = list(iter_jsonl_gz(root / "path_reference_graph.jsonl.gz"))
    path_issues = list(iter_jsonl_gz(root / "path_reference_scan_issues.jsonl.gz"))
    artifact_issues = list(iter_jsonl_gz(root / "artifact_scan_issues.jsonl.gz"))
    consumers = _consumer_inventory(py_imports, mql_includes, doc_links, path_refs)
    write_jsonl_gz(root / "consumer_inventory.jsonl.gz", consumers)
    critical_rows, behavior_manifest = build_critical_logic_inventory(artifacts, py_symbols, mql_symbols, tests)
    write_jsonl_gz(root / "critical_logic_inventory.jsonl.gz", critical_rows)
    write_json(root / "behavior_characterization_manifest.json", behavior_manifest)

    unresolved = list(artifact_issues)
    unresolved.extend({"kind": "python_parse_issue", "path": x["path"], "severity": "BLOCKING" if x.get("production_candidate") else "RECORDED", "details": x} for x in py_issues)
    unresolved.extend({"kind": "mql5_read_issue", "path": x["path"], "severity": "BLOCKING", "details": x} for x in mql_issues)
    unresolved.extend({"kind": "documentation_read_issue", "path": x["path"], "severity": "RECORDED", "details": x} for x in doc_issues)
    unresolved.extend({"kind": "schema_read_issue", "path": x["path"], "severity": "RECORDED", "details": x} for x in schema_issues)
    unresolved.extend({"kind": "path_reference_read_issue", "path": x["path"], "severity": "RECORDED", "details": x} for x in path_issues)
    unresolved.extend({"kind": "documentation_id_collision", "path": x["paths"][0], "severity": "RECORDED", "details": x} for x in doc_collisions)
    if not behavior_manifest["all_critical_artifacts_have_surface_fingerprint"]:
        unresolved.append({"kind": "critical_logic_without_surface_fingerprint", "path": "<multiple>", "severity": "BLOCKING"})
    if not behavior_manifest["all_critical_domains_have_executable_evidence"]:
        unresolved.append({"kind": "critical_domain_without_executable_test_evidence", "path": "<domain-map>", "severity": "BLOCKING", "details": behavior_manifest["domain_coverage"]})
    unresolved = sorted(unresolved, key=lambda x: (x.get("severity", ""), x.get("kind", ""), x.get("path", "")))
    write_jsonl_gz(root / "unresolved_items.jsonl.gz", unresolved)

    snapshot = read_json(root / "repository_snapshot.json")
    root_digest = snapshot["root_digest_sha256"]
    baseline_id = "UC01BASE_" + root_digest[:32].upper()
    manifest = {
        "baseline_id": baseline_id,
        "program_id": "UCPS",
        "stage_id": STAGE_ID,
        "implementation_version": IMPLEMENTATION_VERSION,
        "captured_at": snapshot["captured_at"],
        "repository_root_digest_sha256": root_digest,
        "artifact_count": len(artifacts),
        "python_symbol_count": len(py_symbols),
        "python_import_edge_count": len(py_imports),
        "mql5_symbol_count": len(mql_symbols),
        "mql5_include_edge_count": len(mql_includes),
        "documentation_count": len(docs),
        "documentation_link_count": len(doc_links),
        "schema_count": len(schemas),
        "consumer_edge_count": len(consumers),
        "critical_logic_count": len(critical_rows),
        "test_symbol_count": len(tests),
        "unresolved_item_count": len(unresolved),
        "blocking_item_count": sum(1 for x in unresolved if x.get("severity") == "BLOCKING"),
        "claim_ceiling": "Complete static and preservation baseline; no migration, semantic unification, cutover, deletion, runtime, order, or capital authority.",
        "immutable": True,
    }
    write_json(root / "baseline_manifest.json", manifest)
    for name, value in {
        "preservation_receipt.json": {"status": "PENDING", "reason": "run preserve command"},
        "recovery_drill_receipt.json": {"status": "PENDING", "reason": "run recovery-drill command"},
        "qualification_receipt.json": {"status": "PENDING", "reason": "run qualify command"},
        "no_destructive_change_receipt.json": _baseline_stabilization_receipt(repo_root),
        "stage_exit_decision.json": {"status": "PENDING", "reason": "preservation, recovery and qualification not yet complete"},
        "uc02_handoff.json": {"status": "NOT_ISSUED", "reason": "UC-01 exit decision not accepted"},
    }.items():
        path = root / name
        if not path.exists():
            write_json(path, value)
    details = {"baseline_id": baseline_id, "consumer_edge_count": len(consumers), "critical_logic_count": len(critical_rows), "blocking_item_count": manifest["blocking_item_count"], "duration_seconds": round(time.time() - started, 3)}
    _record_step(root, "assemble", "PASS", details)
    generate_commit_index(repo_root, root)
    return details


def capture_baseline(repo_root: Path, baseline_root: Path | None = None, *, allow_existing: bool = False) -> dict:
    repo_root = repo_root.resolve()
    root = (baseline_root or repo_root / BASELINE_RELATIVE_ROOT).resolve()
    if root.exists() and any(root.iterdir()) and not allow_existing:
        raise FileExistsError(f"immutable baseline directory already contains files: {root}")
    root.mkdir(parents=True, exist_ok=True)
    results = {
        "artifacts": capture_artifacts(repo_root, root),
        "python": capture_python_surface(repo_root, root),
        "mql5": capture_mql5_surface(repo_root, root),
        "documents": capture_documents_and_schemas(repo_root, root),
        "references": capture_path_references(repo_root, root),
        "assemble": assemble_baseline(repo_root, root),
    }
    _write_hash_ledger(root)
    return {"status": "CAPTURED", "baseline_root": str(root), "steps": results, **results["assemble"]}


def resume_capture(repo_root: Path, root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    state = _load_state(root)
    results = {}
    for step, function in (
        ("artifacts", capture_artifacts),
        ("python", capture_python_surface),
        ("mql5", capture_mql5_surface),
        ("documents", capture_documents_and_schemas),
        ("references", capture_path_references),
        ("assemble", assemble_baseline),
    ):
        if state.get("steps", {}).get(step, {}).get("status") in {"PASS", "BLOCKED"}:
            results[step] = {"status": "REUSED"}
            continue
        results[step] = function(repo_root, root)
        state = _load_state(root)
    return {"status": "CAPTURED", "baseline_root": str(root), "steps": results}


def preserve_baseline(repo_root: Path, baseline_root: Path, preservation_root: Path, *, overwrite_artifacts: bool = False) -> dict:
    manifest = read_json(baseline_root / "baseline_manifest.json")
    preservation_root.mkdir(parents=True, exist_ok=True)
    git_receipt = create_git_preservation(repo_root, preservation_root, tag_name="pre-unified-consolidation", branch_name="archive/pre-unified-consolidation", overwrite_artifacts=overwrite_artifacts)
    archive_receipt = create_source_archive(repo_root, baseline_root / "artifact_inventory.jsonl.gz", preservation_root / f"{manifest['baseline_id']}_SOURCE.zip", overwrite=overwrite_artifacts)
    pre_patch_source = preservation_root / "decision-alpha-lab-pre-unified-consolidation-source.zip"
    if pre_patch_source.is_file():
        import zipfile
        try:
            with zipfile.ZipFile(pre_patch_source, "r") as archive:
                first_bad_member = archive.testzip()
                pre_patch_member_count = len(archive.infolist())
            pre_patch_receipt = {
                "status": "PASS" if first_bad_member is None else "FAILED",
                "archive_path": str(pre_patch_source.resolve()),
                "archive_size": pre_patch_source.stat().st_size,
                "archive_sha256": sha256_file(pre_patch_source),
                "member_count": pre_patch_member_count,
                "first_bad_member": first_bad_member,
                "captured_before_patch_overlay": True,
            }
        except Exception as exc:
            pre_patch_receipt = {
                "status": "FAILED",
                "archive_path": str(pre_patch_source.resolve()),
                "reason": f"{type(exc).__name__}: {exc}",
                "captured_before_patch_overlay": True,
            }
    else:
        pre_patch_receipt = {
            "status": "BLOCKED",
            "reason": "pre_patch_source_archive_missing",
            "expected_path": str(pre_patch_source.resolve()),
            "captured_before_patch_overlay": True,
        }
    preservation_status = (
        "PASS"
        if git_receipt.get("status") == "PASS"
        and archive_receipt.get("status") == "PASS"
        and pre_patch_receipt.get("status") == "PASS"
        else "BLOCKED"
    )
    receipt = {
        "status": preservation_status,
        "baseline_id": manifest["baseline_id"],
        "git_preservation": git_receipt,
        "pre_patch_source_archive": pre_patch_receipt,
        "post_repair_baseline_source_archive": archive_receipt,
        "source_archive": archive_receipt,
        "external_storage_required": True,
        "external_artifacts_committed_to_git": False,
    }
    write_json(baseline_root / "preservation_receipt.json", receipt)
    _write_hash_ledger(baseline_root)
    return receipt


def run_recovery(baseline_root: Path) -> dict:
    preservation = read_json(baseline_root / "preservation_receipt.json")
    archive_text = preservation.get("source_archive", {}).get("archive_path")
    if not archive_text:
        receipt = {"status": "BLOCKED", "reason": "source_archive_not_available"}
    else:
        receipt = recovery_drill(baseline_root / "artifact_inventory.jsonl.gz", Path(archive_text))
        bundle = preservation.get("git_preservation", {}).get("bundle_path")
        if bundle:
            result = run_command(("git", "bundle", "verify", bundle), baseline_root, timeout=300)
            receipt["git_bundle_verify_returncode"] = result.returncode
            receipt["git_bundle_verify_output"] = result.stdout.strip()
            if result.returncode != 0:
                receipt["status"] = "FAILED"
        pre_patch = preservation.get("pre_patch_source_archive", {})
        receipt["pre_patch_source_archive_status"] = pre_patch.get("status", "BLOCKED")
        receipt["pre_patch_source_archive_sha256"] = pre_patch.get("archive_sha256")
        if pre_patch.get("status") != "PASS":
            receipt["status"] = "FAILED" if pre_patch.get("status") == "FAILED" else "BLOCKED"
    write_json(baseline_root / "recovery_drill_receipt.json", receipt)
    _write_hash_ledger(baseline_root)
    return receipt


def qualify(repo_root: Path, baseline_root: Path, *, include_full_regression: bool = True) -> dict:
    receipt = run_qualification(repo_root, include_full_regression=include_full_regression)
    write_json(baseline_root / "qualification_receipt.json", receipt)
    _write_hash_ledger(baseline_root)
    return receipt


def finalize(repo_root: Path, baseline_root: Path) -> dict:
    manifest = read_json(baseline_root / "baseline_manifest.json")
    summary = read_json(baseline_root / "artifact_inventory_summary.json")
    behavior = read_json(baseline_root / "behavior_characterization_manifest.json")
    preservation = read_json(baseline_root / "preservation_receipt.json")
    recovery = read_json(baseline_root / "recovery_drill_receipt.json")
    qualification = read_json(baseline_root / "qualification_receipt.json")
    no_destructive = read_json(baseline_root / "no_destructive_change_receipt.json")
    unresolved = list(iter_jsonl_gz(baseline_root / "unresolved_items.jsonl.gz"))
    blocking = [x for x in unresolved if x.get("severity") == "BLOCKING"]
    gates = {
        "artifact_hash_and_classification": "PASS" if summary["file_count"] == manifest["artifact_count"] and not any(x.get("kind") == "artifact_hash_failure" for x in blocking) else "FAILED",
        "symbol_and_logic_inventory": "PASS" if manifest["python_symbol_count"] + manifest["mql5_symbol_count"] > 0 else "FAILED",
        "lfs_materialization": "PASS" if summary["lfs_pointer_count"] == 0 and not any(x["kind"] in {"lfs_not_materialized", "unmaterialized_lfs_pointer"} for x in blocking) else "BLOCKED",
        "critical_behavior_characterization": "PASS" if behavior["all_critical_artifacts_have_surface_fingerprint"] and behavior["all_critical_domains_have_executable_evidence"] else "BLOCKED",
        "git_and_source_preservation": preservation.get("status", "BLOCKED"),
        "clean_restore": recovery.get("status", "BLOCKED"),
        "qualification": qualification.get("status", "BLOCKED"),
        "no_destructive_change": no_destructive.get("status", "FAILED"),
    }
    status = "FAILED" if any(x == "FAILED" for x in gates.values()) else "BLOCKED" if any(x != "PASS" for x in gates.values()) or blocking else "ACCEPTED"
    decision = {"program_id": "UCPS", "stage_id": STAGE_ID, "baseline_id": manifest["baseline_id"], "status": status, "gates": gates, "blocking_item_count": len(blocking), "blocking_items": blocking[:100], "destructive_authority": False, "uc02_authorized": status == "ACCEPTED", "decision_rule": "Non-compensatory: every required gate must PASS and no blocking item may remain."}
    write_json(baseline_root / "stage_exit_decision.json", decision)
    write_json(baseline_root / "uc02_handoff.json", {"status": "ISSUED" if status == "ACCEPTED" else "NOT_ISSUED", "from_stage": "UC-01", "to_stage": "UC-02", "baseline_id": manifest["baseline_id"], "repository_root_digest_sha256": manifest["repository_root_digest_sha256"], "artifact_inventory": "artifact_inventory.jsonl.gz", "symbol_inventories": ["python_symbol_inventory.jsonl.gz", "mql5_symbol_inventory.jsonl.gz"], "dependency_and_consumer_graphs": ["python_import_graph.jsonl.gz", "mql5_include_graph.jsonl.gz", "consumer_inventory.jsonl.gz"], "behavior_characterization": "behavior_characterization_manifest.json", "unresolved_items": "unresolved_items.jsonl.gz", "claim_ceiling": "UC-02 may assign authority and standards only. Move, merge, cutover and deletion remain forbidden."})
    _write_hash_ledger(baseline_root)
    generate_commit_index(repo_root, baseline_root)
    return decision


def generate_commit_index(repo_root: Path, baseline_root: Path) -> Path:
    static_index = repo_root / RELEASE_RELATIVE_ROOT / "UC01_PATCH_FILE_INDEX.txt"
    paths = [line.strip().replace("\\", "/") for line in static_index.read_text(encoding="utf-8").splitlines() if line.strip()]
    paths.extend(path.relative_to(repo_root).as_posix() for path in sorted(baseline_root.iterdir()) if path.is_file())
    commit_index = baseline_root / "UC01_COMMIT_FILE_INDEX.txt"
    paths.append(commit_index.relative_to(repo_root).as_posix())
    commit_index.write_text("\n".join(sorted(set(paths))) + "\n", encoding="utf-8", newline="\n")
    _write_hash_ledger(baseline_root)
    return commit_index
