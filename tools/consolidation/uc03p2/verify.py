from __future__ import annotations

import argparse
import ast
import importlib
import json
import os
import sys
from pathlib import Path

from .apply import ACTIVE_REWRITE_ROOTS, DIRECTORY_RULES, EXCLUDED_DIRS, FILE_RULES, TEXT_EXTENSIONS, TOOL_SHIMS

REQUIRED_DESTINATIONS = (
    "src/engine/packages",
    "src/engine/legacy/core",
    "src/engine/tooling/strategy_factory",
    "contexts/legacy",
    "tests/legacy",
    "mql5/legacy/strategy_factory_lab",
)


def iter_python(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [item for item in dirnames if item not in EXCLUDED_DIRS and item != ".git"]
        current = Path(dirpath)
        for filename in filenames:
            if filename.endswith(".py"):
                yield current / filename


def syntax_errors(repo: Path) -> list[str]:
    errors: list[str] = []
    roots = (
        repo / "src/engine",
        repo / "contexts/legacy",
        repo / "adapters/legacy",
        repo / "tests/legacy",
        repo / "tools",
    )
    for root in roots:
        if not root.exists():
            continue
        for path in iter_python(root):
            try:
                ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
            except (SyntaxError, UnicodeDecodeError) as exc:
                errors.append(f"python parse failure: {path.relative_to(repo)}: {exc}")
    return errors


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
    probes = []
    for item in preferred + candidates[:8]:
        if item in candidates and item not in probes:
            probes.append(item)
    for name in probes:
        try:
            importlib.import_module(name)
        except Exception as exc:  # import compatibility is the contract under test
            errors.append(f"import probe failed: {name}: {type(exc).__name__}: {exc}")

    for name in ("tools.strategy_factory", "tools.strategy_factory.lcm", "tools.strategy_factory.acl_os"):
        try:
            importlib.import_module(name)
        except Exception as exc:
            errors.append(f"compatibility import failed: {name}: {type(exc).__name__}: {exc}")
    return errors


def verify(repo: Path) -> dict:
    repo = repo.resolve()
    errors: list[str] = []
    decision = repo / "registry/consolidation/uc03/part2/part2_exit_decision.json"
    if not decision.is_file():
        errors.append("part2 exit decision is missing")
    else:
        data = json.loads(decision.read_text(encoding="utf-8"))
        if data.get("status") != "ACCEPTED" or not data.get("uc03_part3_authorized"):
            errors.append("part2 exit decision is not accepted")
        if data.get("uc04_authorized"):
            errors.append("part2 must not authorize UC-04")

    lab = repo / "lab"
    if lab.exists() and any(path.is_file() for path in lab.rglob("*")):
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
            # Some optional source trees may not exist in every checkout.
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
    if len([path for path in repo.iterdir() if path.is_file()]) > 20:
        errors.append("repository root file limit exceeded")

    errors.extend(syntax_errors(repo))
    errors.extend(active_stale_references(repo))
    errors.extend(import_errors(repo))

    result = {
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "lab_file_count": sum(1 for path in lab.rglob("*") if path.is_file()) if lab.exists() else 0,
        "root_file_count": len([path for path in repo.iterdir() if path.is_file()]),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    arguments = parser.parse_args()
    return 0 if verify(Path(arguments.repo_root))["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
