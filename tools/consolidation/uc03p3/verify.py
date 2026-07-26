from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from .apply import (
    DOC_DIRECTORY_RULES,
    DOC_FILE_RULES,
    LEGACY_IMPORT_RULES,
    PART3_ROOT,
    REGISTRY_DIRECTORY_RULES,
    SHIM_PATHS,
    sha256,
)

REQUIRED_DOC_DIRS = (
    "docs/architecture/master",
    "docs/standards/engineering",
    "docs/operations/research",
    "docs/contexts/legacy",
    "docs/history/systems",
)
REQUIRED_REGISTRY_DIRS = (
    "registry/consolidation",
    "registry/history/lcm",
    "registry/history/acl",
    "registry/history/strategy_factory",
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def imported_modules(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return set()
    output: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            output.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            output.add(node.module)
    return output


def verify(repo: Path, ci_fast: bool = False) -> list[str]:
    repo = repo.resolve()
    errors: list[str] = []
    output = repo / PART3_ROOT
    required_receipts = (
        "documentation_relocation_receipt.json",
        "registry_relocation_receipt.json",
        "reference_rewrite_receipt.json",
        "compatibility_usage_report.json",
        "clean_replay_receipt.json",
        "pre_relocation_characterization.json",
        "post_relocation_characterization.json",
        "part3_exit_decision.json",
        "uc04_handoff.json",
    )
    for name in required_receipts:
        if not (output / name).is_file():
            errors.append(f"missing Part 3 receipt: {name}")
    if errors:
        return errors

    decision = read_json(output / "part3_exit_decision.json")
    if decision.get("status") != "ACCEPTED" or decision.get("uc04_authorized") is not True:
        errors.append("UC-03 Part 3 is not accepted or does not authorize UC-04")
    for key in ("deletion_authority", "semantic_merge_authority", "runtime_authority", "order_authority", "capital_authority"):
        if decision.get(key) is True:
            errors.append(f"Part 3 unexpectedly grants {key}")

    for path in REQUIRED_DOC_DIRS + REQUIRED_REGISTRY_DIRS:
        if not (repo / path).is_dir():
            errors.append(f"required physical boundary missing: {path}")
    for source, _ in DOC_DIRECTORY_RULES + REGISTRY_DIRECTORY_RULES:
        path = repo / source
        if path.exists() and any(child.is_file() for child in path.rglob("*")):
            errors.append(f"legacy physical root still contains files: {source}")
    for source, _ in DOC_FILE_RULES:
        if (repo / source).is_file():
            errors.append(f"legacy loose documentation file remains: {source}")

    for relative in SHIM_PATHS:
        path = repo / relative
        if path.exists() or path.parent.exists():
            errors.append(f"compatibility namespace remains after zero-use closure: {path.parent.relative_to(repo)}")

    prefixes = tuple(old for old, _ in LEGACY_IMPORT_RULES)
    roots = (repo / "src", repo / "contexts", repo / "adapters", repo / "tests", repo / "ops", repo / "products", repo / "tools")
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [name for name in dirnames if name not in {".git", "__pycache__", ".pytest_cache"}]
            current = Path(dirpath)
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue
                path = current / filename
                rel = path.relative_to(repo).as_posix()
                if rel.startswith(("tools/consolidation/", "tests/consolidation/")):
                    continue
                for module in imported_modules(path):
                    if any(module == prefix or module.startswith(prefix + ".") for prefix in prefixes):
                        errors.append(f"legacy import remains: {rel}: {module}")
                        if len(errors) > 100:
                            return errors

    for receipt_name in ("documentation_relocation_receipt.json", "registry_relocation_receipt.json"):
        receipt = read_json(output / receipt_name)
        if receipt.get("status") != "PASS" or int(receipt.get("conflict_count", 0)) != 0:
            errors.append(f"relocation receipt is not clean PASS: {receipt_name}")
        rows = receipt.get("relocations", [])
        if len(rows) != int(receipt.get("file_relocation_count", -1)):
            errors.append(f"relocation count mismatch: {receipt_name}")
        sample = rows if not ci_fast else rows[:512]
        for row in sample:
            destination = repo / str(row.get("destination", ""))
            if not destination.is_file():
                errors.append(f"relocated destination missing: {row.get('destination')}")
                continue
            # Rewritten files are validated through the rewrite receipt below.

    rewrite = read_json(output / "reference_rewrite_receipt.json")
    if rewrite.get("status") != "PASS":
        errors.append("reference rewrite receipt is not PASS")
    rewrite_rows = rewrite.get("files", [])
    if len(rewrite_rows) != int(rewrite.get("modified_file_count", -1)):
        errors.append("reference rewrite count mismatch")
    sample_rewrites = rewrite_rows if not ci_fast else rewrite_rows[:512]
    for row in sample_rewrites:
        path = repo / str(row.get("path", ""))
        if not path.is_file() or sha256(path) != str(row.get("after_sha256", "")):
            errors.append(f"rewrite output mismatch: {row.get('path')}")

    clean = read_json(output / "clean_replay_receipt.json")
    if clean.get("status") != "PASS" or clean.get("conflict_count") != 0 or clean.get("errors"):
        errors.append("clean replay did not pass")
    pre = read_json(output / "pre_relocation_characterization.json")
    post = read_json(output / "post_relocation_characterization.json")
    if pre.get("status") != "PASS" or post.get("status") != "PASS":
        errors.append("before/after characterization is not PASS")

    root_file_count = len([path for path in repo.iterdir() if path.is_file()])
    if root_file_count > 20:
        errors.append(f"root file limit exceeded: {root_file_count}")
    if (repo / "lab").exists() and any(path.is_file() for path in (repo / "lab").rglob("*")):
        errors.append("lab contains files after UC-03 closure")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--ci-fast", action="store_true")
    args = parser.parse_args()
    repo = Path(args.repo_root)
    errors = verify(repo, ci_fast=args.ci_fast)
    print(f"UC-03 Part 3 errors: {len(errors)}")
    for item in errors[:100]:
        print("ERROR:", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
