"""Differential root, package and parallel-engine guards for UC-02."""
from __future__ import annotations

import fnmatch
from pathlib import Path, PurePosixPath

import yaml

from .constants import AUTHORITY_ROOT, UC01_BASELINE_ROOT
from .io_utils import iter_jsonl_gz, read_json, write_json


def _repo_files(repo_root: Path) -> list[str]:
    result: list[str] = []
    authority_prefix = AUTHORITY_ROOT.as_posix().rstrip("/") + "/"
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        parts = PurePosixPath(rel).parts
        if any(part in {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"} for part in parts) or rel.endswith(".pyc"):
            continue
        if rel.startswith(authority_prefix):
            continue
        result.append(rel)
    return sorted(result)


def _package_key(path: str) -> str:
    parts = PurePosixPath(path).parts
    if not parts:
        return path
    if parts[0] == "lab" and len(parts) >= 4 and parts[1] == "11_strategy_factory" and parts[2] == "python":
        return "/".join(parts[:4])
    if parts[0] == "tools" and len(parts) >= 3:
        return "/".join(parts[:3])
    if parts[0] in {"src", "contexts", "adapters", "mql5", "tests", "docs", "registry", "policies", "contracts", "schemas", "releases"}:
        return "/".join(parts[: min(3, len(parts))])
    return parts[0]


def run_guard(repo_root: Path, *, require_authority_package: bool = False, receipt_path: Path | None = None) -> dict:
    repo_root = repo_root.resolve()
    baseline_root = repo_root / UC01_BASELINE_ROOT
    errors: list[str] = []
    warnings: list[str] = []
    if not baseline_root.is_dir():
        return {"status": "FAILED", "errors": ["UC-01 baseline is missing"], "warnings": []}

    policy_path = repo_root / "policies/platform/root_and_package_guard.yaml"
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    if not isinstance(policy, dict):
        return {"status": "FAILED", "errors": ["root and package guard policy is invalid"], "warnings": []}

    baseline_rows = list(iter_jsonl_gz(baseline_root / "artifact_inventory.jsonl.gz"))
    baseline_paths = {str(row["path"]) for row in baseline_rows}
    baseline_root_files = {path for path in baseline_paths if "/" not in path}
    baseline_top_levels = {PurePosixPath(path).parts[0] for path in baseline_paths if "/" in path}
    baseline_packages = {_package_key(path) for path in baseline_paths}

    current_paths = set(_repo_files(repo_root))
    current_root_files = {path for path in current_paths if "/" not in path}
    current_top_levels = {PurePosixPath(path).parts[0] for path in current_paths if "/" in path}
    current_packages = {_package_key(path) for path in current_paths}

    allowed_top_levels = set(policy.get("future_allowed_top_level_roots", []))
    new_root_files = sorted(current_root_files - baseline_root_files)
    forbidden_patterns = list(policy.get("forbidden_new_root_patterns", []))
    for path in new_root_files:
        if any(fnmatch.fnmatch(path, pattern) for pattern in forbidden_patterns):
            errors.append(f"forbidden new root release artifact: {path}")
        else:
            errors.append(f"new root file is outside the frozen baseline and allowlist: {path}")

    forbidden_new_top_levels = sorted(current_top_levels - baseline_top_levels - allowed_top_levels)
    if forbidden_new_top_levels:
        errors.append(f"forbidden new top-level roots: {forbidden_new_top_levels}")

    parallel_patterns = list(policy.get("forbidden_new_parallel_engine_patterns", []))
    allowed_tool_roots = set(policy.get("allowed_new_tool_roots", []))
    for package in sorted(current_packages - baseline_packages):
        leaf = PurePosixPath(package).name
        normalized = package.lower()
        if package.startswith(tuple(allowed_tool_roots)):
            continue
        if any(fnmatch.fnmatch(leaf.lower(), pattern.lower()) for pattern in parallel_patterns):
            errors.append(f"forbidden new parallel engine package: {package}")
        if "alpha_lab" in PurePosixPath(package).parts:
            errors.append(f"forbidden nested product package: {package}")
        if package.startswith("lab/") and ("engine" in normalized or "factory" in normalized or "os" in normalized):
            errors.append(f"new production-like package under lab is forbidden: {package}")

    for path in sorted(current_paths - baseline_paths):
        if "/alpha_lab/" in f"/{path}/" or path.startswith("alpha_lab/") or path.startswith("src/alpha_lab/"):
            errors.append(f"forbidden nested Alpha Lab product path: {path}")

    authority_package = repo_root / AUTHORITY_ROOT
    if require_authority_package and not (authority_package / "stage_exit_decision.json").is_file():
        errors.append("accepted UC-02 authority package is required but missing")
    if require_authority_package and (authority_package / "stage_exit_decision.json").is_file():
        decision = read_json(authority_package / "stage_exit_decision.json")
        if decision.get("status") != "ACCEPTED" or decision.get("uc03_authorized") is not True:
            errors.append("UC-02 authority package is not accepted")

    result = {
        "status": "PASS" if not errors else "FAILED",
        "errors": errors,
        "warnings": warnings,
        "baseline_root_file_count": len(baseline_root_files),
        "current_root_file_count": len(current_root_files),
        "new_root_file_count": len(new_root_files),
        "baseline_package_count": len(baseline_packages),
        "current_package_count": len(current_packages),
        "new_package_count": len(current_packages - baseline_packages),
        "destructive_authority": False,
    }
    if receipt_path:
        write_json(receipt_path, result)
    return result
