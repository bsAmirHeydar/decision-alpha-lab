from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Iterable

from .apply import ACTIVE_REWRITE_ROOTS, DIRECTORY_RULES, EXCLUDED_DIRS, FILE_RULES, TEXT_EXTENSIONS, TOOL_SHIMS

REQUIRED_DESTINATIONS = (
    "src/engine/packages",
    "src/engine/legacy/core",
    "src/engine/tooling/strategy_factory",
    "contexts/legacy",
    "tests/legacy",
    "mql5/legacy/strategy_factory_lab",
)

RELOCATION_RECEIPT = Path("registry/consolidation/uc03/part2/code_relocation_receipt.json")
REWRITE_RECEIPT = Path("registry/consolidation/uc03/part2/compatibility_rewrite_receipt.json")
DECISION_PATH = Path("registry/consolidation/uc03/part2/part2_exit_decision.json")


def _read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_python(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [item for item in dirnames if item not in EXCLUDED_DIRS and item != ".git"]
        current = Path(dirpath)
        for filename in filenames:
            if filename.endswith(".py"):
                yield current / filename


def _parse_paths(repo: Path, paths: Iterable[Path]) -> list[str]:
    errors: list[str] = []
    seen: set[Path] = set()
    for path in paths:
        path = path.resolve()
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            errors.append(f"python parse failure: {path.relative_to(repo)}: {exc}")
    return errors


def syntax_errors(repo: Path) -> list[str]:
    roots = (
        repo / "src/engine",
        repo / "contexts/legacy",
        repo / "adapters/legacy",
        repo / "tests/legacy",
        repo / "tools",
    )
    return _parse_paths(repo, (path for root in roots if root.exists() for path in iter_python(root)))


def active_stale_references(repo: Path) -> list[str]:
    stale: list[str] = []
    tokens = [source for source, _ in DIRECTORY_RULES] + [source for source, _ in FILE_RULES]
    exclusions = (
        "tools/consolidation/uc01/",
        "tools/consolidation/uc02/",
        "tools/consolidation/uc03p1/",
        "tools/consolidation/uc03p2/",
        "tests/consolidation/uc01/",
        "tests/consolidation/uc02/",
        "tests/consolidation/uc03p1/",
        "tests/consolidation/uc03p2/",
        "tools/engineering/audit_repository_layout.py",
        "tools/repository_paths.py",
        "sitecustomize.py",
        "releases/unified_consolidation/uc03/part2/",
        "registry/consolidation/uc03/part2/",
        "docs/alpha_lab_master_architecture/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/12_UC03_PHYSICAL_REORGANIZATION_RECORDS/",
    )
    for relative_root in ACTIVE_REWRITE_ROOTS:
        root = repo / relative_root
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [item for item in dirnames if item not in EXCLUDED_DIRS]
            current = Path(dirpath)
            for filename in filenames:
                path = current / filename
                relative = path.relative_to(repo).as_posix()
                if relative.startswith(exclusions):
                    continue
                if path.suffix.lower() not in TEXT_EXTENSIONS and filename not in {".gitignore", ".gitattributes"}:
                    continue
                try:
                    text = path.read_text(encoding="utf-8-sig")
                except (UnicodeDecodeError, OSError):
                    continue
                scrubbed = text
                for _, destination in DIRECTORY_RULES:
                    scrubbed = scrubbed.replace(destination, "")
                    scrubbed = scrubbed.replace(destination.replace("/", "\\"), "")
                for _, destination in FILE_RULES:
                    scrubbed = scrubbed.replace(destination, "")
                    scrubbed = scrubbed.replace(destination.replace("/", "\\"), "")
                for token in tokens:
                    if token in scrubbed or token.replace("/", "\\") in scrubbed:
                        stale.append(f"stale active reference: {relative}: {token}")
                        break
    return stale


def import_errors(repo: Path) -> list[str]:
    errors: list[str] = []
    paths = (
        repo / "src/engine/packages",
        repo / "src/engine/legacy/core",
        repo / "src/engine/legacy/infrastructure/utils",
    )
    for path in reversed(paths):
        if path.is_dir() and str(path) not in sys.path:
            sys.path.insert(0, str(path))

    packages_root = repo / "src/engine/packages"
    candidates: list[str] = []
    if packages_root.is_dir():
        candidates = sorted(
            child.name for child in packages_root.iterdir()
            if child.is_dir() and (child / "__init__.py").is_file()
        )
    preferred = [
        "strategy_factory_context",
        "strategy_factory_statistics",
        "strategy_factory_validation",
        "strategy_factory_research",
    ]
    probes: list[str] = []
    for item in preferred + candidates[:8]:
        if item in candidates and item not in probes:
            probes.append(item)
    for name in probes:
        try:
            importlib.import_module(name)
        except Exception as exc:
            errors.append(f"import probe failed: {name}: {type(exc).__name__}: {exc}")

    for name in ("tools.strategy_factory", "tools.strategy_factory.lcm", "tools.strategy_factory.acl_os"):
        try:
            importlib.import_module(name)
        except Exception as exc:
            errors.append(f"compatibility import failed: {name}: {type(exc).__name__}: {exc}")
    return errors


def _base_topology_errors(repo: Path) -> tuple[list[str], int, int]:
    errors: list[str] = []
    decision = repo / DECISION_PATH
    if not decision.is_file():
        errors.append("part2 exit decision is missing")
    else:
        data = _read_json(decision)
        if data.get("status") != "ACCEPTED" or not data.get("uc03_part3_authorized"):
            errors.append("part2 exit decision is not accepted")
        if data.get("uc04_authorized"):
            errors.append("part2 must not authorize UC-04")
        for key in ("deletion_authority", "semantic_merge_authority", "runtime_authority", "order_authority", "capital_authority"):
            if data.get(key) is True:
                errors.append(f"part2 decision unexpectedly grants {key}")

    lab = repo / "lab"
    lab_file_count = sum(1 for path in lab.rglob("*") if path.is_file()) if lab.exists() else 0
    if lab_file_count:
        errors.append("lab still contains files")

    for destination in REQUIRED_DESTINATIONS:
        if not (repo / destination).is_dir():
            errors.append(f"required destination is missing: {destination}")

    shim_sources = {source for source, _ in TOOL_SHIMS}
    for source, destination in DIRECTORY_RULES:
        source_path = repo / source
        destination_path = repo / destination
        if source not in shim_sources and source_path.exists() and any(path.is_file() for path in source_path.rglob("*")):
            errors.append(f"source still contains files: {source}")
        if not destination_path.exists():
            continue

    for old, _ in TOOL_SHIMS:
        shim = repo / old
        files = sorted(
            path.relative_to(shim).as_posix()
            for path in shim.rglob("*") if path.is_file() and "__pycache__" not in path.parts
        ) if shim.is_dir() else []
        if files != ["__init__.py"]:
            errors.append(f"tool compatibility namespace contains unexpected files: {old}: {files}")

    if not (repo / "sitecustomize.py").is_file():
        errors.append("sitecustomize.py compatibility bootstrap is missing")
    root_file_count = len([path for path in repo.iterdir() if path.is_file()])
    if root_file_count > 20:
        errors.append("repository root file limit exceeded")
    return errors, lab_file_count, root_file_count


def fast_receipt_errors(repo: Path) -> list[str]:
    errors: list[str] = []
    relocation_path = repo / RELOCATION_RECEIPT
    rewrite_path = repo / REWRITE_RECEIPT
    if not relocation_path.is_file():
        return ["code relocation receipt is missing"]
    if not rewrite_path.is_file():
        return ["compatibility rewrite receipt is missing"]

    relocation = _read_json(relocation_path)
    rewrite = _read_json(rewrite_path)
    if relocation.get("status") != "PASS" or int(relocation.get("conflict_count", 0)) != 0:
        errors.append("code relocation receipt is not a clean PASS")
    if rewrite.get("status") != "PASS":
        errors.append("compatibility rewrite receipt is not PASS")

    relocation_rows = relocation.get("relocations", [])
    if not isinstance(relocation_rows, list) or len(relocation_rows) != int(relocation.get("file_relocation_count", -1)):
        errors.append("code relocation receipt count mismatch")
        relocation_rows = []

    python_candidates: list[Path] = []
    for row in relocation_rows:
        if not isinstance(row, dict):
            errors.append("invalid relocation row")
            continue
        destination = str(row.get("destination", ""))
        path = repo / destination
        if not destination or not path.is_file():
            errors.append(f"relocated destination is missing: {destination}")
            if len(errors) >= 50:
                return errors
            continue
        if destination.endswith(".py"):
            python_candidates.append(path)

    rewrite_rows = rewrite.get("files", [])
    if not isinstance(rewrite_rows, list) or len(rewrite_rows) != int(rewrite.get("modified_file_count", -1)):
        errors.append("rewrite receipt count mismatch")
        rewrite_rows = []
    rewritten_python: list[Path] = []
    for row in rewrite_rows:
        if not isinstance(row, dict):
            errors.append("invalid rewrite row")
            continue
        relative = str(row.get("path", ""))
        expected = str(row.get("after_sha256", "")).lower()
        path = repo / relative
        if not relative or not path.is_file():
            errors.append(f"rewritten file is missing: {relative}")
            continue
        if expected and _sha256(path) != expected:
            errors.append(f"rewritten file hash mismatch: {relative}")
        if relative.endswith(".py"):
            rewritten_python.append(path)

    # CI parses every rewritten Python file plus a deterministic relocation sample.
    sampled = sorted(python_candidates, key=lambda item: item.as_posix())[:256]
    errors.extend(_parse_paths(repo, [*rewritten_python, *sampled]))
    return errors


def verify(repo: Path, *, ci_fast: bool = False) -> dict:
    repo = repo.resolve()
    errors, lab_file_count, root_file_count = _base_topology_errors(repo)
    if ci_fast:
        errors.extend(fast_receipt_errors(repo))
        errors.extend(import_errors(repo))
    else:
        errors.extend(syntax_errors(repo))
        errors.extend(active_stale_references(repo))
        errors.extend(import_errors(repo))

    result = {
        "status": "PASS" if not errors else "FAIL",
        "mode": "CI_FAST" if ci_fast else "FULL",
        "error_count": len(errors),
        "errors": errors,
        "lab_file_count": lab_file_count,
        "root_file_count": root_file_count,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--ci-fast", action="store_true")
    arguments = parser.parse_args()
    return 0 if verify(Path(arguments.repo_root), ci_fast=arguments.ci_fast)["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
