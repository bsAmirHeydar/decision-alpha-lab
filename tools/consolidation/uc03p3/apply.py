from __future__ import annotations

import argparse
import ast
import codecs
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

TEXT_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".csv", ".sha256", ".ps1", ".bat", ".cmd", ".mq5",
    ".mqh", ".xml", ".html", ".js", ".ts", ".tsx", ".jsx", ".sql",
    ".rst", ".properties", ".env", ".lock", ".canvas",
}
EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache",
}

DOC_DIRECTORY_RULES: tuple[tuple[str, str], ...] = (
    ("docs/alpha_lab_master_architecture", "docs/architecture/master"),
    ("docs/ai_algorithm_engineering_os", "docs/history/aieos_legacy"),
    ("docs/engineering", "docs/standards/engineering"),
    ("docs/knowledge", "docs/standards/knowledge"),
    ("docs/articles", "docs/standards/articles"),
    ("docs/process", "docs/operations/process"),
    ("docs/research", "docs/operations/research"),
    ("docs/evidence", "docs/operations/evidence"),
    ("docs/execution", "docs/operations/execution"),
    ("docs/ui", "docs/operations/ui"),
    ("docs/mql_native", "docs/operations/mql5_native"),
    ("docs/ai_execution", "docs/operations/ai_execution"),
    ("docs/experience_capture", "docs/contexts/legacy/experience_capture"),
    ("docs/flag_counting", "docs/contexts/legacy/flag_counting"),
    ("docs/hook_validity", "docs/contexts/legacy/hook_validity"),
    ("docs/nds_entry_architecture", "docs/contexts/legacy/nds/entry"),
    ("docs/nds_hook_architecture", "docs/contexts/legacy/nds/hook"),
    ("docs/zone_af", "docs/contexts/legacy/zone_af"),
    ("docs/obsidian", "docs/history/obsidian/base"),
    ("docs/obsidian_deep", "docs/history/obsidian/deep"),
    ("docs/obsidian_hook", "docs/history/obsidian/hook"),
    ("docs/obsidian_zone", "docs/history/obsidian/zone"),
    ("docs/debug", "docs/history/debug"),
    ("docs/generated", "docs/history/generated"),
    ("docs/patches", "docs/history/delivery/patches"),
    ("docs/releases", "docs/history/delivery/releases"),
    ("docs/reports", "docs/history/reports"),
    ("docs/root_archive", "docs/history/root_archive"),
    ("docs/strategy_factory", "docs/history/systems/strategy_factory"),
    ("docs/strategy_factory_context_intelligence_edge_discovery_v3", "docs/history/systems/saed_v3"),
    ("docs/strategy_factory_implementation", "docs/history/systems/strategy_factory_implementation"),
    ("docs/strategy_factory_implementation_roadmap", "docs/history/systems/strategy_factory_roadmap"),
    ("docs/strategy_factory_setup_ai_edge_discovery", "docs/history/systems/setup_ai_v1"),
    ("docs/strategy_factory_setup_ai_edge_discovery_institutional_v2", "docs/history/systems/setup_ai_v2"),
    ("docs/strategy_factory_sovereign_context_intelligence_v4", "docs/history/systems/saed_v4"),
    ("docs/strategy_factory_universal_context_exploitation_engine", "docs/history/systems/ucee"),
    ("docs/strategy_factory_v2", "docs/history/systems/strategy_factory_v2"),
)

DOC_FILE_RULES: tuple[tuple[str, str], ...] = (
    ("docs/00_project_index.md", "docs/README.md"),
    ("docs/architecture.md", "docs/architecture/overview.md"),
    ("docs/laboratory_architecture.md", "docs/architecture/laboratory.md"),
    ("docs/PROJECT_LAYOUT.md", "docs/architecture/project_layout.md"),
    ("docs/atomic_live_research_contract.md", "docs/standards/atomic_live_research_contract.md"),
    ("docs/glossary.md", "docs/standards/glossary.md"),
    ("docs/manifesto.md", "docs/standards/manifesto.md"),
    ("docs/principles.md", "docs/standards/principles.md"),
    ("docs/research-roadmap.md", "docs/operations/research/roadmap.md"),
    ("docs/research_lessons_and_failure_modes.md", "docs/operations/research/lessons_and_failure_modes.md"),
    ("docs/astro_ml_training_quickstart.md", "docs/operations/research/astro_ml_training_quickstart.md"),
    ("docs/EXP0015_cme_live_backtest_plan.md", "docs/contexts/legacy/exp0015/cme_live_backtest_plan.md"),
    ("docs/EXP0015_cme_live_provider_patch.md", "docs/contexts/legacy/exp0015/cme_live_provider_patch.md"),
    ("docs/MQL_LIVE_ALL_IN_ONE_APPLY.md", "docs/contexts/legacy/mql_visual/live_all_in_one_apply.md"),
    ("docs/MQL_NATIVE_MIGRATION_DECISION.md", "docs/contexts/legacy/mql_visual/native_migration_decision.md"),
    ("docs/mql_live_visual_lab.md", "docs/contexts/legacy/mql_visual/live_visual_lab.md"),
    ("docs/mql_live_visual_lab_debug_packages.md", "docs/contexts/legacy/mql_visual/live_visual_lab_debug_packages.md"),
    ("docs/mql_visual_lab.md", "docs/contexts/legacy/mql_visual/visual_lab.md"),
)

REGISTRY_DIRECTORY_RULES: tuple[tuple[str, str], ...] = (
    ("registry/legacy_context_migration", "registry/history/lcm"),
    ("registry/acl_os", "registry/history/acl"),
    ("registry/strategy_factory", "registry/history/strategy_factory"),
    ("registry/patches", "registry/history/patches"),
    ("registry/releases", "registry/history/releases"),
)

LEGACY_IMPORT_RULES: tuple[tuple[str, str], ...] = (
    ("tools.strategy_factory", "src.engine.tooling.strategy_factory"),
    ("tools.cme_bridge", "adapters.legacy.market_data.cme_bridge"),
    ("tools.astro_live_bridge", "adapters.legacy.market_data.astro_live_bridge"),
    ("tools.astro_feature_builder", "src.engine.legacy.research.astro_feature_builder"),
    ("tools.astro_ml", "src.engine.legacy.research.astro_ml"),
    ("tools.astro_validation", "tests.legacy.astro_validation"),
    ("tools.flag_counting", "contexts.legacy.tools.flag_counting"),
    ("tools.exp0019", "contexts.legacy.tools.exp0019"),
    ("tools.stc_smt_deployment", "ops.deployment.stc_smt"),
    ("tools.alpha_lens_mobile", "products.alpha_lens_mobile.tools"),
)

SHIM_PATHS = tuple(name.replace(".", "/") + "/__init__.py" for name, _ in LEGACY_IMPORT_RULES)

ACTIVE_REWRITE_ROOTS = (
    ".github", "src", "tools", "tests", "contexts", "adapters", "configs", "ops",
    "policies", "contracts", "schemas", "mql5", "products", "examples",
    "docs/architecture", "docs/standards", "docs/operations", "docs/contexts",
    "registry/consolidation", "releases/unified_consolidation",
)
ACTIVE_ROOT_FILES = ("README.md", "AGENTS.md", "CONTRIBUTING.md")

REWRITE_EXCLUDED_PREFIXES = (
    "tools/consolidation/uc03p3/",
    "tests/consolidation/uc03p3/",
    "registry/consolidation/uc03/part1/",
    "registry/consolidation/uc03/part2/",
    "registry/consolidation/uc03/part3/",
    "releases/unified_consolidation/",
    "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/_release/",
)

PART2_DECISION = "registry/consolidation/uc03/part2/part2_exit_decision.json"
PART3_ROOT = "registry/consolidation/uc03/part3"
RELEASE_ROOT = "releases/unified_consolidation/uc03/part3"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".uc03p3.tmp")
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def write_json(path: Path, payload: dict) -> None:
    atomic_write(path, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def iter_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return ()
    return (path for path in root.rglob("*") if path.is_file())


def conflict_path(repo: Path, destination: Path, digest: str) -> Path:
    relative = destination.relative_to(repo)
    candidate = repo / "releases/history/conflicts/uc03_part3" / relative.parent / (
        f"{relative.stem}__{digest[:12]}{relative.suffix}"
    )
    index = 1
    while candidate.exists():
        candidate = repo / "releases/history/conflicts/uc03_part3" / relative.parent / (
            f"{relative.stem}__{digest[:12]}_{index}{relative.suffix}"
        )
        index += 1
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


def move_file(repo: Path, source_rel: str, destination_rel: str, domain: str) -> tuple[dict | None, str | None]:
    source = repo / source_rel
    destination = repo / destination_rel
    if not source.is_file():
        if destination.is_file():
            return None, None
        return None, f"missing source and destination: {source_rel} -> {destination_rel}"
    before = sha256(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    status = "MOVED"
    conflict: str | None = None
    if destination.exists():
        existing = sha256(destination)
        if existing == before:
            source.unlink()
            status = "DUPLICATE_SOURCE_REMOVED"
        else:
            saved = conflict_path(repo, destination, existing)
            shutil.move(str(destination), str(saved))
            conflict = saved.relative_to(repo).as_posix()
            shutil.move(str(source), str(destination))
            status = "MOVED_DESTINATION_CONFLICT_PRESERVED"
    else:
        shutil.move(str(source), str(destination))
    if not destination.is_file() or sha256(destination) != before:
        return None, f"byte-preserving move failed: {source_rel}"
    return {
        "source": source_rel,
        "destination": destination_rel,
        "source_sha256": before,
        "status": status,
        "domain": domain,
    }, conflict


def move_tree(repo: Path, source_rel: str, destination_rel: str, domain: str) -> tuple[list[dict], list[str], list[str]]:
    source_root = repo / source_rel
    destination_root = repo / destination_rel
    rows: list[dict] = []
    conflicts: list[str] = []
    errors: list[str] = []
    if source_root.is_file():
        return rows, conflicts, [f"directory source is a file: {source_rel}"]

    # Fast path: a whole-tree rename on the same volume is atomic and does not
    # modify file bytes. This is the normal path on the user's repository.
    if source_root.is_dir() and not destination_root.exists():
        destination_root.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.replace(source_root, destination_root)
        except OSError:
            shutil.move(str(source_root), str(destination_root))
        for destination in sorted(iter_files(destination_root), key=lambda p: p.as_posix()):
            child = destination.relative_to(destination_root).as_posix()
            rows.append({
                "source": f"{source_rel}/{child}",
                "destination": f"{destination_rel}/{child}",
                "source_sha256": sha256(destination),
                "status": "MOVED_TREE_ATOMIC",
                "domain": domain,
            })
        return rows, conflicts, errors

    # Resume path: the source may already be gone and the accepted destination
    # may already exist after an interrupted run.
    if not source_root.exists() and destination_root.is_dir():
        for destination in sorted(iter_files(destination_root), key=lambda p: p.as_posix()):
            child = destination.relative_to(destination_root).as_posix()
            rows.append({
                "source": f"{source_rel}/{child}",
                "destination": f"{destination_rel}/{child}",
                "source_sha256": sha256(destination),
                "status": "ALREADY_MOVED",
                "domain": domain,
            })
        return rows, conflicts, errors

    if not source_root.exists():
        return rows, conflicts, errors

    # Collision/partial-resume path. It is slower but preserves both sides.
    for source in sorted(iter_files(source_root), key=lambda p: p.as_posix()):
        child = source.relative_to(source_root).as_posix()
        row, conflict = move_file(repo, f"{source_rel}/{child}", f"{destination_rel}/{child}", domain)
        if row:
            rows.append(row)
        if conflict:
            conflicts.append(conflict)
        if row is None and not (repo / f"{destination_rel}/{child}").is_file():
            errors.append(f"move failed: {source_rel}/{child}")
    for current, dirs, files in os.walk(source_root, topdown=False):
        try:
            Path(current).rmdir()
        except OSError:
            pass
    return rows, conflicts, errors


def decode_text(path: Path) -> tuple[str, str, bool] | None:
    raw = path.read_bytes()
    if b"\x00" in raw[:4096]:
        return None
    bom = raw.startswith(codecs.BOM_UTF8)
    body = raw[len(codecs.BOM_UTF8):] if bom else raw
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return None
    newline = "\r\n" if b"\r\n" in body else "\n"
    return text, newline, bom


def encode_text(text: str, newline: str, bom: bool) -> bytes:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    payload = normalized.replace("\n", newline).encode("utf-8")
    return (codecs.BOM_UTF8 + payload) if bom else payload


def path_replacements() -> list[tuple[str, str]]:
    rules = list(DOC_DIRECTORY_RULES) + list(DOC_FILE_RULES) + list(REGISTRY_DIRECTORY_RULES)
    output: list[tuple[str, str]] = []
    for old, new in rules:
        output.append((old, new))
        output.append((old.replace("/", "\\"), new.replace("/", "\\")))
    output.extend((
        ("alpha_lab_master_architecture/", "architecture/master/"),
        ("alpha_lab_master_architecture\\", "architecture\\master\\"),
    ))
    return sorted(set(output), key=lambda row: len(row[0]), reverse=True)


def compiled_path_replacements() -> list[tuple[re.Pattern[str], str, str]]:
    boundary = r"(?<![A-Za-z0-9_./\\-])"
    return [(re.compile(boundary + re.escape(old)), old, new) for old, new in path_replacements()]


def compiled_import_replacements() -> list[tuple[re.Pattern[str], str]]:
    """Match legacy module roots only, never a suffix of an already-migrated import."""
    boundary = r"(?<![A-Za-z0-9_.])"
    return [
        (re.compile(boundary + re.escape(old)), new)
        for old, new in LEGACY_IMPORT_RULES
    ]


def iter_active_text_files(repo: Path) -> Iterable[Path]:
    seen: set[Path] = set()
    for relative_root in ACTIVE_REWRITE_ROOTS:
        root = repo / relative_root
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS and name != "history"]
            current = Path(dirpath)
            for filename in filenames:
                path = current / filename
                rel = path.relative_to(repo).as_posix()
                if rel.startswith(REWRITE_EXCLUDED_PREFIXES):
                    continue
                if path.suffix.lower() not in TEXT_EXTENSIONS and filename not in {".gitignore", ".gitattributes"}:
                    continue
                if path not in seen:
                    seen.add(path)
                    yield path
    for relative in ACTIVE_ROOT_FILES:
        path = repo / relative
        if path.is_file() and path not in seen:
            yield path


def rewrite_active_files(repo: Path) -> tuple[list[dict], int]:
    path_rules = compiled_path_replacements()
    import_rules = compiled_import_replacements()
    rows: list[dict] = []
    total = 0
    for path in sorted(iter_active_text_files(repo), key=lambda p: p.as_posix()):
        decoded = decode_text(path)
        if decoded is None:
            continue
        text, newline, bom = decoded
        updated = text
        count = 0
        kinds: set[str] = set()
        for pattern, old, new in path_rules:
            if old not in updated:
                continue
            updated, occurrences = pattern.subn(lambda _: new, updated)
            if occurrences:
                count += occurrences
                kinds.add("PATH")
        for pattern, new in import_rules:
            updated, occurrences = pattern.subn(new, updated)
            count += occurrences
            if occurrences:
                kinds.add("IMPORT")
        if updated == text:
            continue
        before = sha256(path)
        atomic_write(path, encode_text(updated, newline, bom))
        after = sha256(path)
        rows.append({
            "path": path.relative_to(repo).as_posix(),
            "before_sha256": before,
            "after_sha256": after,
            "replacement_count": count,
            "kinds": sorted(kinds),
        })
        total += count
    return rows, total


def imported_module_names(path: Path) -> set[str]:
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


def legacy_import_usage(repo: Path) -> list[dict]:
    prefixes = tuple(old for old, _ in LEGACY_IMPORT_RULES)
    usage: list[dict] = []
    roots = (repo / "src", repo / "contexts", repo / "adapters", repo / "tests", repo / "ops", repo / "products", repo / "tools")
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
            current = Path(dirpath)
            for filename in filenames:
                if not filename.endswith(".py"):
                    continue
                path = current / filename
                rel = path.relative_to(repo).as_posix()
                if rel.startswith(("tools/consolidation/", "tests/consolidation/")) or rel in SHIM_PATHS:
                    continue
                for module in imported_module_names(path):
                    if any(module == prefix or module.startswith(prefix + ".") for prefix in prefixes):
                        usage.append({"path": rel, "module": module})
    return usage


def retire_shims(repo: Path) -> list[str]:
    retired: list[str] = []
    for relative in SHIM_PATHS:
        path = repo / relative
        directory = path.parent
        if path.is_file():
            path.unlink()
            retired.append(relative)
        if directory.is_dir():
            remaining = [item for item in directory.rglob("*") if item.is_file() and "__pycache__" not in item.parts and item.suffix != ".pyc"]
            if remaining:
                raise RuntimeError(f"compatibility namespace contains non-shim files: {directory.relative_to(repo)}")
            shutil.rmtree(directory)
    return retired


def run_command(repo: Path, command: list[str]) -> dict:
    proc = subprocess.run(command, cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output = proc.stdout or ""
    return {
        "command": command,
        "return_code": proc.returncode,
        "output_sha256": hashlib.sha256(output.encode("utf-8", errors="replace")).hexdigest(),
        "output_tail": output[-4000:],
    }


def characterization(repo: Path, phase: str) -> dict:
    commands: list[list[str]] = [
        [sys.executable, "-m", "tools.consolidation.uc03p2.verify", "--repo-root", ".", "--ci-fast"],
        [sys.executable, "-m", "tools.consolidation.uc03p3.probe", "--repo-root", "."],
    ]
    if phase == "POST_RELOCATION":
        commands.extend((
            [sys.executable, "-m", "tools.consolidation.uc02.cli", "verify-static-patch", "--repo-root", "."],
            [sys.executable, "-m", "tools.consolidation.ci.verify_migration_continuity", "--repo-root", "."],
            [sys.executable, "tools/engineering/run_engineering_policy.py", "."],
        ))
    rows = [run_command(repo, command) for command in commands]
    return {"phase": phase, "status": "PASS" if all(row["return_code"] == 0 for row in rows) else "FAIL", "commands": rows}


def git_tracked_paths(repo: Path) -> set[str]:
    proc = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", "-z"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git tracked-path enumeration failed: {proc.stderr.decode('utf-8', errors='replace')}")
    return {
        value.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        for value in proc.stdout.split(b"\0")
        if value
    }


def receipt_rows(repo: Path, name: str, field: str) -> list[dict]:
    path = repo / PART3_ROOT / name
    if not path.is_file():
        return []
    payload = read_json(path)
    values = payload.get(field, [])
    return values if isinstance(values, list) else []


def build_commit_paths(repo: Path) -> list[str]:
    """Build a compact, exact staging pathspec set for UC-03 Part 3.

    A per-file list for more than thirty-five thousand renames is needlessly
    slow on Windows. Whole-tree relocations are staged with their exact source
    and destination directory pathspecs; rewritten files and static controls
    remain individually scoped. The repository is required to be clean before
    applying the patch, so these bounded pathspecs cannot absorb unrelated work.
    """
    tracked = git_tracked_paths(repo)
    paths: set[str] = set()

    for source, destination in DOC_DIRECTORY_RULES + REGISTRY_DIRECTORY_RULES:
        paths.add(source)
        paths.add(destination)

    for source, destination in DOC_FILE_RULES:
        if source in tracked:
            paths.add(source)
        paths.add(destination)

    for row in receipt_rows(repo, "reference_rewrite_receipt.json", "files"):
        value = str(row.get("path", "")).replace("\\", "/")
        if value:
            paths.add(value)

    compatibility = repo / PART3_ROOT / "compatibility_usage_report.json"
    if compatibility.is_file():
        for value in read_json(compatibility).get("retired_shims", []):
            value = str(value).replace("\\", "/")
            if value:
                paths.add(value)

    static_index = repo / RELEASE_ROOT / "STATIC_PATCH_FILE_INDEX.txt"
    if static_index.is_file():
        for line in static_index.read_text(encoding="utf-8-sig").splitlines():
            value = line.strip().replace("\\", "/")
            if not value:
                continue
            # Static notes under the relocated master-vault tree are already
            # covered by the directory source/destination pathspecs.
            if value.startswith("docs/alpha_lab_master_architecture/"):
                continue
            if value in tracked or (repo / value).exists():
                paths.add(value)

    paths.add(PART3_ROOT)
    paths.add(RELEASE_ROOT)
    conflict_root = "releases/history/conflicts/uc03_part3"
    if (repo / conflict_root).exists():
        paths.add(conflict_root)

    return sorted(paths)


def write_commit_index(repo: Path) -> list[str]:
    paths = build_commit_paths(repo)
    index_path = repo / RELEASE_ROOT / "PATCH_FILE_INDEX.txt"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(paths) + "\n", encoding="utf-8", newline="\n")
    return paths


def apply(repo: Path) -> dict:
    repo = repo.resolve()
    part2 = repo / PART2_DECISION
    if not part2.is_file():
        raise RuntimeError("UC-03 Part 2 exit decision is missing")
    decision = read_json(part2)
    if decision.get("status") != "ACCEPTED" or decision.get("uc03_part3_authorized") is not True:
        raise RuntimeError("UC-03 Part 2 has not authorized Part 3")

    output_root = repo / PART3_ROOT
    output_root.mkdir(parents=True, exist_ok=True)

    accepted_path = output_root / "part3_exit_decision.json"
    required_receipts = (
        output_root / "documentation_relocation_receipt.json",
        output_root / "registry_relocation_receipt.json",
        output_root / "reference_rewrite_receipt.json",
        output_root / "compatibility_usage_report.json",
        output_root / "clean_replay_receipt.json",
        output_root / "uc04_handoff.json",
    )
    if accepted_path.is_file() and all(path.is_file() for path in required_receipts):
        accepted = read_json(accepted_path)
        if accepted.get("status") == "ACCEPTED" and accepted.get("uc04_authorized") is True:
            documentation = read_json(required_receipts[0])
            registry = read_json(required_receipts[1])
            rewrite = read_json(required_receipts[2])
            compatibility = read_json(required_receipts[3])
            final_paths = write_commit_index(repo)
            return {
                "status": "ACCEPTED",
                "documentation_relocation_count": int(documentation.get("file_relocation_count", 0)),
                "registry_relocation_count": int(registry.get("file_relocation_count", 0)),
                "rewrite_file_count": int(rewrite.get("modified_file_count", 0)),
                "replacement_count": int(rewrite.get("replacement_count", 0)),
                "retired_shim_count": int(compatibility.get("retired_shim_count", 0)),
                "commit_path_count": len(final_paths),
                "uc04_authorized": True,
                "resume_mode": "ACCEPTED_INDEX_REBUILD",
            }

    # A previous bounded run may already have produced the immutable relocation
    # and replay evidence but stopped before issuing the exit decision.  Never
    # recompute those receipts: doing so from the relocated tree loses their
    # before/after lineage.  Re-characterize the current tree, then issue the
    # decision only when the preserved evidence and current checks both pass.
    evidence_paths = (
        output_root / "documentation_relocation_receipt.json",
        output_root / "registry_relocation_receipt.json",
        output_root / "reference_rewrite_receipt.json",
        output_root / "compatibility_usage_report.json",
        output_root / "clean_replay_receipt.json",
    )
    if all(path.is_file() for path in evidence_paths):
        documentation, registry, rewrite, compatibility, clean = (
            read_json(path) for path in evidence_paths
        )
        evidence_valid = (
            documentation.get("status") == "PASS"
            and registry.get("status") == "PASS"
            and rewrite.get("status") == "PASS"
            and compatibility.get("status") == "PASS"
            and compatibility.get("usage_count") == 0
            and clean.get("status") == "PASS"
            and clean.get("conflict_count") == 0
            and not clean.get("errors")
        )
        if evidence_valid:
            post = characterization(repo, "POST_RELOCATION")
            write_json(output_root / "post_relocation_characterization.json", post)
            if post["status"] != "PASS":
                raise RuntimeError("post-relocation characterization failed")
            write_json(accepted_path, {
                "schema_version": "1.0.0", "program_id": "UCPS", "stage_id": "UC-03", "part_id": "UC03-P3",
                "status": "ACCEPTED", "uc03_closed": True, "uc04_authorized": True,
                "deletion_authority": False, "semantic_merge_authority": False,
                "runtime_authority": False, "order_authority": False, "capital_authority": False,
            })
            write_json(output_root / "uc04_handoff.json", {
                "schema_version": "1.0.0", "program_id": "UCPS", "from_stage": "UC-03", "to_stage": "UC-04",
                "status": "ISSUED", "authorized_scope": "SEMANTIC_UNIFICATION_WITHOUT_UNPROVEN_LOGIC_RETIREMENT",
                "required_inputs": [
                    "registry/consolidation/uc03/part1/root_relocation_receipt.json",
                    "registry/consolidation/uc03/part2/code_relocation_receipt.json",
                    "registry/consolidation/uc03/part3/documentation_relocation_receipt.json",
                    "registry/consolidation/uc03/part3/registry_relocation_receipt.json",
                    "registry/consolidation/uc03/part3/clean_replay_receipt.json",
                ],
            })
            final_paths = write_commit_index(repo)
            return {
                "status": "ACCEPTED",
                "documentation_relocation_count": int(documentation.get("file_relocation_count", 0)),
                "registry_relocation_count": int(registry.get("file_relocation_count", 0)),
                "rewrite_file_count": int(rewrite.get("modified_file_count", 0)),
                "replacement_count": int(rewrite.get("replacement_count", 0)),
                "retired_shim_count": int(compatibility.get("retired_shim_count", 0)),
                "commit_path_count": len(final_paths),
                "uc04_authorized": True,
                "resume_mode": "EVIDENCE_FINALIZATION",
            }

    state_path = output_root / "apply_state.json"
    state = read_json(state_path) if state_path.is_file() else {}
    pre_path = output_root / "pre_relocation_characterization.json"
    if state.get("pre_characterization") == "PASS" and pre_path.is_file():
        pre = read_json(pre_path)
    else:
        pre = characterization(repo, "PRE_RELOCATION")
        write_json(pre_path, pre)
        if pre["status"] != "PASS":
            raise RuntimeError("pre-relocation characterization failed")
        state["pre_characterization"] = "PASS"
        write_json(state_path, state)

    baseline_rows: list[dict] = []
    move_rows: list[dict] = []
    conflicts: list[str] = []
    errors: list[str] = []

    for source, destination in DOC_DIRECTORY_RULES:
        rows, found_conflicts, found_errors = move_tree(repo, source, destination, "DOCUMENTATION")
        baseline_rows.extend(rows)
        move_rows.extend(rows)
        conflicts.extend(found_conflicts)
        errors.extend(found_errors)
    for source, destination in DOC_FILE_RULES:
        row, conflict = move_file(repo, source, destination, "DOCUMENTATION")
        if row:
            baseline_rows.append(row)
            move_rows.append(row)
        if conflict:
            conflicts.append(conflict)
    for source, destination in REGISTRY_DIRECTORY_RULES:
        rows, found_conflicts, found_errors = move_tree(repo, source, destination, "REGISTRY")
        baseline_rows.extend(rows)
        move_rows.extend(rows)
        conflicts.extend(found_conflicts)
        errors.extend(found_errors)

    if errors:
        raise RuntimeError("; ".join(errors[:20]))

    rewrite_rows, replacement_count = rewrite_active_files(repo)
    legacy_usage = legacy_import_usage(repo)
    if legacy_usage:
        write_json(output_root / "compatibility_usage_report.json", {
            "schema_version": "1.0.0", "status": "BLOCKED", "usage_count": len(legacy_usage), "usage": legacy_usage,
        })
        raise RuntimeError(f"legacy compatibility imports remain: {len(legacy_usage)}")
    retired = retire_shims(repo)

    documentation_rows = [row for row in move_rows if row["domain"] == "DOCUMENTATION"]
    registry_rows = [row for row in move_rows if row["domain"] == "REGISTRY"]
    write_json(output_root / "documentation_relocation_receipt.json", {
        "schema_version": "1.0.0", "program_id": "UCPS", "stage_id": "UC-03", "part_id": "UC03-P3",
        "status": "PASS", "file_relocation_count": len(documentation_rows), "conflict_count": len(conflicts),
        "relocations": documentation_rows,
    })
    write_json(output_root / "registry_relocation_receipt.json", {
        "schema_version": "1.0.0", "program_id": "UCPS", "stage_id": "UC-03", "part_id": "UC03-P3",
        "status": "PASS", "file_relocation_count": len(registry_rows), "conflict_count": len(conflicts),
        "relocations": registry_rows,
    })
    write_json(output_root / "reference_rewrite_receipt.json", {
        "schema_version": "1.0.0", "status": "PASS", "modified_file_count": len(rewrite_rows),
        "replacement_count": replacement_count, "files": rewrite_rows,
    })
    write_json(output_root / "compatibility_usage_report.json", {
        "schema_version": "1.0.0", "status": "PASS", "usage_count": 0,
        "retired_shim_count": len(retired), "retired_shims": retired,
        "semantic_merge_authority": False,
    })

    release_root = repo / RELEASE_ROOT
    uc02_amended_paths = []
    for relative in (
        "tools/consolidation/uc02/verify.py",
    ):
        target = repo / relative
        if target.is_file():
            uc02_amended_paths.append({"path": relative, "sha256": sha256(target)})
    write_json(release_root / "UC02_STATIC_AMENDMENT.json", {
        "schema_version": "1.0.0", "program_id": "UCPS", "stage_id": "UC-03",
        "part_id": "UC03-P3", "upstream_stage": "UC-02",
        "deletion_authority": False, "semantic_merge_authority": False,
        "runtime_authority": False, "order_authority": False,
        "broker_authority": False, "capital_authority": False,
        "amended_paths": uc02_amended_paths,
    })

    foundation_amendments = []
    for historical, current in (
        (
            "docs/alpha_lab_master_architecture/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/03_EXECUTION_STAGES/03_UC03_Reorganize_Physically.md",
            "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/03_EXECUTION_STAGES/03_UC03_Reorganize_Physically.md",
        ),
        (
            "docs/alpha_lab_master_architecture/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/12_UC03_PHYSICAL_REORGANIZATION_RECORDS/00_MOC.md",
            "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/12_UC03_PHYSICAL_REORGANIZATION_RECORDS/00_MOC.md",
        ),
        (
            "docs/alpha_lab_master_architecture/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/tools/validate_program_vault.py",
            "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/tools/validate_program_vault.py",
        ),
        (
            "tools/engineering/run_engineering_policy.py",
            "tools/engineering/run_engineering_policy.py",
        ),
    ):
        target = repo / current
        if target.is_file():
            foundation_amendments.append({
                "historical_path": historical, "path": current, "sha256": sha256(target),
            })
    write_json(release_root / "OBSIDIAN_FOUNDATION_AMENDMENT.json", {
        "schema_version": "1.0.0", "program_id": "UCPS", "stage_id": "UC-03",
        "part_id": "UC03-P3", "amended_paths": foundation_amendments,
    })

    # Virtual clean replay: every moved input is accounted for by a destination,
    # and every rewritten destination is connected through a before/after hash.
    rewrite_by_path = {row["path"]: row for row in rewrite_rows}
    replay_errors: list[str] = []
    for row in baseline_rows:
        destination = repo / row["destination"]
        if not destination.is_file():
            replay_errors.append(f"missing destination: {row['destination']}")
            continue
        rewrite = rewrite_by_path.get(row["destination"])
        if rewrite:
            if rewrite["before_sha256"] != row["source_sha256"]:
                replay_errors.append(f"rewrite chain mismatch: {row['destination']}")
            if sha256(destination) != rewrite["after_sha256"]:
                replay_errors.append(f"rewrite output mismatch: {row['destination']}")
        # A whole-tree rename is byte-preserving and the relocation receipt hash
        # was calculated from the accepted destination immediately after the move.
        # Rewritten files are checked above; unrewritten files only need to remain present.
    write_json(output_root / "clean_replay_receipt.json", {
        "schema_version": "1.0.0", "status": "PASS" if not replay_errors and not conflicts else "FAIL",
        "baseline_artifact_count": len(baseline_rows), "accounted_artifact_count": len(baseline_rows) - len(replay_errors),
        "conflict_count": len(conflicts), "errors": replay_errors, "conflict_paths": conflicts,
    })
    if replay_errors or conflicts:
        raise RuntimeError("UC-03 Part 3 clean replay failed")

    post = characterization(repo, "POST_RELOCATION")
    write_json(output_root / "post_relocation_characterization.json", post)
    if post["status"] != "PASS":
        raise RuntimeError("post-relocation characterization failed")

    write_json(output_root / "part3_exit_decision.json", {
        "schema_version": "1.0.0", "program_id": "UCPS", "stage_id": "UC-03", "part_id": "UC03-P3",
        "status": "ACCEPTED", "uc03_closed": True, "uc04_authorized": True,
        "deletion_authority": False, "semantic_merge_authority": False,
        "runtime_authority": False, "order_authority": False, "capital_authority": False,
    })
    write_json(output_root / "uc04_handoff.json", {
        "schema_version": "1.0.0", "program_id": "UCPS", "from_stage": "UC-03", "to_stage": "UC-04",
        "status": "ISSUED", "authorized_scope": "SEMANTIC_UNIFICATION_WITHOUT_UNPROVEN_LOGIC_RETIREMENT",
        "required_inputs": [
            "registry/consolidation/uc03/part1/root_relocation_receipt.json",
            "registry/consolidation/uc03/part2/code_relocation_receipt.json",
            "registry/consolidation/uc03/part3/documentation_relocation_receipt.json",
            "registry/consolidation/uc03/part3/registry_relocation_receipt.json",
            "registry/consolidation/uc03/part3/clean_replay_receipt.json",
        ],
    })

    # Build the staging set directly from signed receipts. This avoids a slow
    # repository-wide diff over tens of thousands of renames on Windows.
    final_paths = write_commit_index(repo)

    return {
        "status": "ACCEPTED",
        "documentation_relocation_count": len(documentation_rows),
        "registry_relocation_count": len(registry_rows),
        "rewrite_file_count": len(rewrite_rows),
        "replacement_count": replacement_count,
        "retired_shim_count": len(retired),
        "commit_path_count": len(final_paths),
        "uc04_authorized": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    result = apply(Path(args.repo_root))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
