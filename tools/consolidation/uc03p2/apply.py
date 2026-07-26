from __future__ import annotations

import argparse
import codecs
import hashlib
import json
import os
import re
import shutil
import subprocess
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
REWRITE_EXCLUDED_FILES = {
    "tools/engineering/audit_repository_layout.py",
    "tools/repository_paths.py",
    "sitecustomize.py",
}

REWRITE_EXCLUDED_PREFIXES = (
    "tools/consolidation/uc01/",
    "tools/consolidation/uc02/",
    "tools/consolidation/uc03p1/",
    "tools/consolidation/uc03p2/",
    "tests/consolidation/uc01/",
    "tests/consolidation/uc02/",
    "tests/consolidation/uc03p1/",
    "tests/consolidation/uc03p2/",
    "releases/unified_consolidation/uc03/part2/",
    "registry/consolidation/uc03/part2/",
    "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/12_UC03_PHYSICAL_REORGANIZATION_RECORDS/",
)

ACTIVE_REWRITE_ROOTS = (
    ".github", "src", "tools", "tests", "contexts", "adapters", "configs",
    "ops", "policies", "contracts", "schemas", "mql5", "products", "examples",
    "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL",
    "docs/architecture/master/00_START_HERE",
)

# Physical-only relocation.  The legacy namespace is intentional until UC-04.
DIRECTORY_RULES: tuple[tuple[str, str], ...] = (
    ("lab/11_strategy_factory/python", "src/engine/packages"),
    ("lab/11_strategy_factory/acl_os", "src/engine/legacy/acl_os_reference"),
    ("lab/11_strategy_factory/phase02_runtime", "src/engine/legacy/strategy_factory/runtime"),
    ("lab/11_strategy_factory/phase03_market", "src/engine/legacy/strategy_factory/market"),
    ("lab/11_strategy_factory/phase04_plugins", "adapters/legacy/strategy_factory_plugins"),
    ("lab/11_strategy_factory/phase01_contracts", "contracts/legacy/strategy_factory"),
    ("lab/11_strategy_factory/schemas", "schemas/legacy/strategy_factory"),
    ("lab/11_strategy_factory/contexts", "contexts/legacy/strategy_factory/authored"),
    ("lab/11_strategy_factory/generated_contexts", "contexts/legacy/strategy_factory/generated"),
    ("lab/11_strategy_factory/tests", "tests/legacy/strategy_factory/v1"),
    ("lab/11_strategy_factory/tests_v2", "tests/legacy/strategy_factory/v2"),
    ("lab/11_strategy_factory/test_vectors", "tests/fixtures/legacy/strategy_factory"),
    ("lab/11_strategy_factory/migration", "tests/legacy/strategy_factory/migration"),
    ("lab/11_strategy_factory/mql5", "mql5/legacy/strategy_factory_lab"),
    ("lab/11_strategy_factory/examples", "examples/legacy/strategy_factory"),
    ("lab/11_strategy_factory/artifacts", "releases/history/strategy_factory/artifacts"),
    ("lab/11_strategy_factory/phase00_current_state_audit", "releases/history/strategy_factory/program/current_state_audit"),
    ("lab/11_strategy_factory/implementation_program", "releases/history/strategy_factory/program/implementation"),
    ("lab/11_strategy_factory/phase_status", "releases/history/strategy_factory/program/status"),
    ("lab/core", "src/engine/legacy/core"),
    ("lab/01_observation", "contexts/legacy/research/observation"),
    ("lab/02_hypotheses", "contexts/legacy/research/hypotheses"),
    ("lab/03_experiments", "contexts/legacy/lab_experiments"),
    ("lab/03_validation", "tests/legacy/validation/research"),
    ("lab/04_analysis", "src/engine/legacy/research/analysis"),
    ("lab/04_execution", "src/engine/legacy/execution/families"),
    ("lab/05_validation", "tests/legacy/validation/qualification"),
    ("lab/06_production", "src/engine/legacy/production"),
    ("lab/07_monitoring", "src/engine/legacy/monitoring"),
    ("lab/08_archive", "releases/history/lab_archive"),
    ("lab/09_execution", "src/engine/legacy/execution/runtime"),
    ("lab/10_infrastructure/EXP0018_daye_trader", "contexts/legacy/infrastructure/exp0018_daye_trader"),
    ("lab/10_infrastructure/EXP0019_faerie_protocol", "contexts/legacy/infrastructure/exp0019_faerie_protocol"),
    ("lab/10_infrastructure/tests", "tests/legacy/infrastructure"),
    ("lab/10_infrastructure/config", "configs/legacy/infrastructure"),
    ("lab/10_infrastructure/ci", "ops/ci/legacy"),
    ("lab/10_infrastructure/data", "data/legacy/infrastructure"),
    ("lab/10_infrastructure/utils", "src/engine/legacy/infrastructure/utils"),
    ("tools/strategy_factory", "src/engine/tooling/strategy_factory"),
    ("tools/cme_bridge", "adapters/legacy/market_data/cme_bridge"),
    ("tools/astro_live_bridge", "adapters/legacy/market_data/astro_live_bridge"),
    ("tools/astro_feature_builder", "src/engine/legacy/research/astro_feature_builder"),
    ("tools/astro_ml", "src/engine/legacy/research/astro_ml"),
    ("tools/astro_validation", "tests/legacy/astro_validation"),
    ("tools/flag_counting", "contexts/legacy/tools/flag_counting"),
    ("tools/exp0019", "contexts/legacy/tools/exp0019"),
    ("tools/stc_smt_deployment", "ops/deployment/stc_smt"),
    ("tools/alpha_lens_mobile", "products/alpha_lens_mobile/tools"),
    ("mql5/Experts/StrategyFactoryTests", "mql5/Tests/Experts/StrategyFactory"),
    ("mql5/Experts/FaerieProtocolTests", "mql5/Tests/Experts/FaerieProtocol"),
    ("mql5/Experts/EXP0019/FaerieProtocolTests", "mql5/Tests/Experts/EXP0019/FaerieProtocol"),
    ("mql5/Indicators/EXP0019/FaerieProtocolTests", "mql5/Tests/Indicators/EXP0019/FaerieProtocol"),
)

FILE_RULES: tuple[tuple[str, str], ...] = (
    ("lab/11_strategy_factory/sf.py", "src/engine/legacy/strategy_factory/sf.py"),
    ("lab/11_strategy_factory/requirements-optional.txt", "configs/dependencies/strategy_factory-optional.txt"),
    ("lab/11_strategy_factory/README.md", "releases/history/strategy_factory/program/README.md"),
    ("lab/11_strategy_factory/README_V2.md", "releases/history/strategy_factory/program/README_V2.md"),
)

TOOL_SHIMS: tuple[tuple[str, str], ...] = (
    ("tools/strategy_factory", "src/engine/tooling/strategy_factory"),
    ("tools/cme_bridge", "adapters/legacy/market_data/cme_bridge"),
    ("tools/astro_live_bridge", "adapters/legacy/market_data/astro_live_bridge"),
    ("tools/astro_feature_builder", "src/engine/legacy/research/astro_feature_builder"),
    ("tools/astro_ml", "src/engine/legacy/research/astro_ml"),
    ("tools/astro_validation", "tests/legacy/astro_validation"),
    ("tools/flag_counting", "contexts/legacy/tools/flag_counting"),
    ("tools/exp0019", "contexts/legacy/tools/exp0019"),
    ("tools/stc_smt_deployment", "ops/deployment/stc_smt"),
    ("tools/alpha_lens_mobile", "products/alpha_lens_mobile/tools"),
)

ROOT_PARENT_PATTERNS = (
    re.compile(r"Path\(__file__\)\.resolve\(\)\.parents\[(\d+)\]"),
    re.compile(r"Path\(__file__\)\.parents\[(\d+)\]"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
    temporary = path.with_name(path.name + ".uc03p2.tmp")
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def conflict_path(repo: Path, destination: Path, digest: str) -> Path:
    relative = destination.relative_to(repo)
    candidate = repo / "releases/history/conflicts/uc03_part2" / relative.parent / (
        f"{relative.stem}__{digest[:12]}{relative.suffix}"
    )
    index = 1
    while candidate.exists():
        candidate = repo / "releases/history/conflicts/uc03_part2" / relative.parent / (
            f"{relative.stem}__{digest[:12]}_{index}{relative.suffix}"
        )
        index += 1
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


def iter_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return ()
    return (path for path in root.rglob("*") if path.is_file())


def move_tree(repo: Path, source_rel: str, destination_rel: str) -> tuple[list[dict], list[str]]:
    source_root = repo / source_rel
    destination_root = repo / destination_rel
    records: list[dict] = []
    conflicts: list[str] = []

    if source_root.is_file():
        raise RuntimeError(f"directory rule source is a file: {source_rel}")

    if source_root.exists():
        files = sorted(iter_files(source_root), key=lambda item: item.as_posix())
        for source in files:
            child = source.relative_to(source_root)
            destination = destination_root / child
            destination.parent.mkdir(parents=True, exist_ok=True)
            before = sha256(source)
            status = "MOVED"
            if destination.exists():
                existing = sha256(destination)
                if existing == before:
                    source.unlink()
                    status = "DUPLICATE_SOURCE_REMOVED"
                else:
                    saved = conflict_path(repo, destination, existing)
                    shutil.move(str(destination), str(saved))
                    conflicts.append(saved.relative_to(repo).as_posix())
                    shutil.move(str(source), str(destination))
                    status = "MOVED_DESTINATION_CONFLICT_PRESERVED"
            else:
                shutil.move(str(source), str(destination))
            if not destination.is_file() or sha256(destination) != before:
                raise RuntimeError(f"byte-preserving move failed: {source.relative_to(repo)}")
            records.append({
                "source": source.relative_to(repo).as_posix(),
                "destination": destination.relative_to(repo).as_posix(),
                "source_sha256": before,
                "status": status,
            })
        for directory in sorted(
            (path for path in source_root.rglob("*") if path.is_dir()),
            key=lambda item: len(item.parts),
            reverse=True,
        ):
            try:
                directory.rmdir()
            except OSError:
                pass
        try:
            source_root.rmdir()
        except OSError:
            pass
    elif destination_root.exists():
        for destination in sorted(iter_files(destination_root), key=lambda item: item.as_posix()):
            child = destination.relative_to(destination_root)
            records.append({
                "source": (Path(source_rel) / child).as_posix(),
                "destination": destination.relative_to(repo).as_posix(),
                "source_sha256": sha256(destination),
                "status": "ALREADY_MOVED",
            })
    return records, conflicts


def move_file(repo: Path, source_rel: str, destination_rel: str) -> tuple[dict | None, list[str]]:
    source = repo / source_rel
    destination = repo / destination_rel
    conflicts: list[str] = []
    if source.is_file():
        before = sha256(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        status = "MOVED"
        if destination.is_file():
            existing = sha256(destination)
            if existing == before:
                source.unlink()
                status = "DUPLICATE_SOURCE_REMOVED"
            else:
                saved = conflict_path(repo, destination, existing)
                shutil.move(str(destination), str(saved))
                conflicts.append(saved.relative_to(repo).as_posix())
                shutil.move(str(source), str(destination))
                status = "MOVED_DESTINATION_CONFLICT_PRESERVED"
        else:
            shutil.move(str(source), str(destination))
        if sha256(destination) != before:
            raise RuntimeError(f"byte-preserving move failed: {source_rel}")
        return ({
            "source": source_rel,
            "destination": destination_rel,
            "source_sha256": before,
            "status": status,
        }, conflicts)
    if destination.is_file():
        return ({
            "source": source_rel,
            "destination": destination_rel,
            "source_sha256": sha256(destination),
            "status": "ALREADY_MOVED",
        }, conflicts)
    return None, conflicts


def decode_text(raw: bytes) -> tuple[str, bool] | None:
    if b"\x00" in raw[:4096]:
        return None
    bom = raw.startswith(codecs.BOM_UTF8)
    try:
        return raw.decode("utf-8-sig" if bom else "utf-8"), bom
    except UnicodeDecodeError:
        return None


def add_root_import(text: str) -> str:
    statement = "from tools.repository_paths import find_repository_root"
    if statement in text:
        return text
    lines = text.splitlines(keepends=True)
    insertion = 0
    if lines and lines[0].startswith("#!"):
        insertion = 1
    while insertion < len(lines) and "coding" in lines[insertion][:40]:
        insertion += 1
    if insertion < len(lines) and lines[insertion].lstrip().startswith(('"""', "'''")):
        quote = lines[insertion].lstrip()[:3]
        if lines[insertion].count(quote) >= 2 and len(lines[insertion].strip()) > 6:
            insertion += 1
        else:
            insertion += 1
            while insertion < len(lines):
                if quote in lines[insertion]:
                    insertion += 1
                    break
                insertion += 1
    while insertion < len(lines) and lines[insertion].startswith("from __future__ import"):
        insertion += 1
    lines.insert(insertion, statement + "\n")
    return "".join(lines)


def rewrite_root_discovery(repo: Path, move_records: list[dict]) -> list[dict]:
    changes: list[dict] = []
    for record in move_records:
        destination = repo / record["destination"]
        source_virtual = repo / record["source"]
        if destination.suffix.lower() != ".py" or not destination.is_file():
            continue
        raw = destination.read_bytes()
        decoded = decode_text(raw)
        if decoded is None:
            continue
        text, bom = decoded
        updated = text
        replacement_count = 0
        for pattern in ROOT_PARENT_PATTERNS:
            def replace(match: re.Match[str]) -> str:
                nonlocal replacement_count
                depth = int(match.group(1))
                try:
                    resolved = source_virtual.resolve().parents[depth]
                except IndexError:
                    return match.group(0)
                if resolved != repo:
                    return match.group(0)
                replacement_count += 1
                return "find_repository_root(__file__)"
            updated = pattern.sub(replace, updated)
        if replacement_count == 0 or updated == text:
            continue
        updated = add_root_import(updated)
        payload = updated.encode("utf-8")
        if bom:
            payload = codecs.BOM_UTF8 + payload
        before = hashlib.sha256(raw).hexdigest()
        atomic_write(destination, payload)
        changes.append({
            "path": record["destination"],
            "kind": "ROOT_DISCOVERY",
            "replacement_count": replacement_count,
            "before_sha256": before,
            "after_sha256": hashlib.sha256(payload).hexdigest(),
        })
    return changes


def iter_active_text_files(repo: Path) -> Iterable[tuple[Path, str]]:
    for relative_root in ACTIVE_REWRITE_ROOTS:
        root = repo / relative_root
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [item for item in dirnames if item not in EXCLUDED_DIRS]
            current = Path(dirpath)
            relative_dir = current.relative_to(repo).as_posix()
            if relative_dir.startswith("releases/history") or any(
                relative_dir == prefix.rstrip("/") or relative_dir.startswith(prefix)
                for prefix in REWRITE_EXCLUDED_PREFIXES
            ):
                dirnames[:] = []
                continue
            for filename in filenames:
                path = current / filename
                relative = path.relative_to(repo).as_posix()
                if relative in REWRITE_EXCLUDED_FILES or any(
                    relative == f"{source}/__init__.py" for source, _ in TOOL_SHIMS
                ):
                    continue
                if path.suffix.lower() not in TEXT_EXTENSIONS and filename not in {".gitignore", ".gitattributes"}:
                    continue
                yield path, relative


def rewrite_paths(repo: Path) -> list[dict]:
    mapping = dict(DIRECTORY_RULES)
    mapping.update(dict(FILE_RULES))
    ordered = sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True)
    changes: list[dict] = []
    for path, relative in iter_active_text_files(repo):
        raw = path.read_bytes()
        decoded = decode_text(raw)
        if decoded is None:
            continue
        text, bom = decoded
        updated = text
        count = 0
        for source, destination in ordered:
            variants = (
                (source, destination),
                (source.replace("/", "\\"), destination.replace("/", "\\")),
                (source.replace("/", "\\\\"), destination.replace("/", "\\\\")),
            )
            for old, new in variants:
                occurrences = updated.count(old)
                if occurrences:
                    updated = updated.replace(old, new)
                    count += occurrences
        if count == 0 or updated == text:
            continue
        payload = updated.encode("utf-8")
        if bom:
            payload = codecs.BOM_UTF8 + payload
        before = hashlib.sha256(raw).hexdigest()
        atomic_write(path, payload)
        changes.append({
            "path": relative,
            "kind": "PATH_REFERENCE",
            "replacement_count": count,
            "before_sha256": before,
            "after_sha256": hashlib.sha256(payload).hexdigest(),
        })
    return changes


def make_tool_shims(repo: Path) -> list[str]:
    created: list[str] = []
    for old, destination in TOOL_SHIMS:
        package = repo / old
        package.mkdir(parents=True, exist_ok=True)
        init = package / "__init__.py"
        content = (
            '"""Temporary UC-03 compatibility namespace; remove after consumer cutover."""\n'
            "from tools.repository_paths import find_repository_root\n"
            f"__path__ = [str(find_repository_root(__file__) / {destination!r})]\n"
        )
        init.write_text(content, encoding="utf-8")
        created.append(init.relative_to(repo).as_posix())
    return created


def clean_caches(repo: Path) -> None:
    for dirpath, dirnames, filenames in os.walk(repo, topdown=False):
        current = Path(dirpath)
        if ".git" in current.parts:
            continue
        for filename in filenames:
            if filename.endswith(".pyc"):
                (current / filename).unlink(missing_ok=True)
        for dirname in dirnames:
            if dirname in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}:
                shutil.rmtree(current / dirname, ignore_errors=True)


def git_changed_paths(repo: Path) -> set[str] | None:
    if not (repo / ".git").exists():
        return None
    def run(*arguments: str) -> list[str]:
        completed = subprocess.run(
            ["git", "-c", "core.quotepath=false", *arguments],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
        return [
            value.decode("utf-8", errors="surrogateescape").replace("\\", "/")
            for value in completed.stdout.split(b"\0") if value
        ]
    paths = set(run("diff", "--name-only", "-z"))
    paths.update(run("diff", "--cached", "--name-only", "-z"))
    paths.update(run("ls-files", "--others", "--exclude-standard", "-z"))
    return paths


def consolidate_rewrites(changes: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for change in changes:
        path = str(change["path"])
        existing = grouped.get(path)
        if existing is None:
            grouped[path] = dict(change)
            grouped[path]["kinds"] = [str(change["kind"])]
            continue
        if existing.get("after_sha256") != change.get("before_sha256"):
            raise RuntimeError(f"non-contiguous rewrite chain: {path}")
        existing["after_sha256"] = change["after_sha256"]
        existing["replacement_count"] = int(existing.get("replacement_count", 0)) + int(change.get("replacement_count", 0))
        existing["kind"] = "MULTI_STAGE"
        existing.setdefault("kinds", []).append(str(change["kind"]))
    return [grouped[path] for path in sorted(grouped)]


def _ledger_rows(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            digest, relative = line.split("  ", 1)
        except ValueError:
            continue
        rows[relative] = digest
    return rows


def write_upstream_amendments(repo: Path, moves: list[dict]) -> list[str]:
    moved = {str(row["source"]): row for row in moves}
    release = repo / "releases/unified_consolidation/uc03/part2"
    specs = (
        (
            "UC-01",
            repo / "releases/unified_consolidation/uc01/UC01_PATCH_FILE_HASHES.sha256",
            release / "UC01_STATIC_AMENDMENT.json",
        ),
        (
            "UC-02",
            repo / "releases/unified_consolidation/uc02/UC02_PATCH_FILE_HASHES.sha256",
            release / "UC02_STATIC_AMENDMENT.json",
        ),
    )
    written: list[str] = []
    for upstream, ledger_path, output in specs:
        amendments: list[dict] = []
        for relative, expected in sorted(_ledger_rows(ledger_path).items()):
            relocation = moved.get(relative)
            if relocation is not None:
                actual = str(relocation.get("source_sha256", ""))
            else:
                target = repo / relative
                if not target.is_file():
                    continue
                actual = sha256(target)
            if actual and actual != expected:
                amendments.append({"path": relative, "sha256": actual})
        payload = {
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC-03",
            "part_id": "UC03-P2",
            "upstream_stage": upstream,
            "reason": "Bounded physical-relocation amendment generated from the runtime checkout.",
            "amended_paths": amendments,
            "semantic_merge_authority": False,
            "deletion_authority": False,
        }
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append(output.relative_to(repo).as_posix())
    return written


def apply(repo: Path) -> dict:
    repo = repo.resolve()
    part1 = repo / "registry/consolidation/uc03/part1/part1_exit_decision.json"
    if not part1.is_file():
        raise RuntimeError("UC-03 Part 1 accepted receipt is missing")
    part1_data = json.loads(part1.read_text(encoding="utf-8"))
    if part1_data.get("status") != "ACCEPTED" or not part1_data.get("uc03_part2_authorized"):
        raise RuntimeError("UC-03 Part 1 did not authorize Part 2")

    existing_decision = repo / "registry/consolidation/uc03/part2/part2_exit_decision.json"
    if existing_decision.is_file():
        try:
            decision_data = json.loads(existing_decision.read_text(encoding="utf-8"))
        except Exception:
            decision_data = {}
        if decision_data.get("status") == "ACCEPTED" and decision_data.get("uc03_part3_authorized") is True:
            clean_caches(repo)
            release = repo / "releases/unified_consolidation/uc03/part2"
            index = release / "PATCH_FILE_INDEX.txt"
            changed = git_changed_paths(repo)
            if changed is not None:
                changed.add(index.relative_to(repo).as_posix())
                index.write_text("\n".join(sorted(changed)) + "\n", encoding="utf-8")
            return {
                "status": "PASS",
                "already_applied": True,
                "commit_path_count": len(changed) if changed is not None else len(index.read_text(encoding="utf-8").splitlines()) if index.is_file() else 0,
            }

    move_records: list[dict] = []
    conflicts: list[str] = []
    shim_sources = {source for source, _ in TOOL_SHIMS}
    for source, destination in DIRECTORY_RULES:
        source_root = repo / source
        if source in shim_sources and source_root.is_dir():
            source_files = [
                path.relative_to(source_root).as_posix()
                for path in source_root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            ]
            if source_files == ["__init__.py"]:
                content = (source_root / "__init__.py").read_text(encoding="utf-8", errors="ignore")
                if "Temporary UC-03 compatibility namespace" in content:
                    continue
        records, saved = move_tree(repo, source, destination)
        move_records.extend(records)
        conflicts.extend(saved)
    for source, destination in FILE_RULES:
        record, saved = move_file(repo, source, destination)
        if record:
            move_records.append(record)
        conflicts.extend(saved)

    # Remove empty lab hierarchy after all controlled moves.
    lab = repo / "lab"
    if lab.exists():
        for directory in sorted((item for item in lab.rglob("*") if item.is_dir()), key=lambda item: len(item.parts), reverse=True):
            try:
                directory.rmdir()
            except OSError:
                pass
        try:
            lab.rmdir()
        except OSError:
            pass

    root_changes = rewrite_root_discovery(repo, move_records)
    path_changes = rewrite_paths(repo)
    shims = make_tool_shims(repo)
    clean_caches(repo)

    receipt_root = repo / "registry/consolidation/uc03/part2"
    receipt_root.mkdir(parents=True, exist_ok=True)
    move_receipt = receipt_root / "code_relocation_receipt.json"
    rewrite_receipt = receipt_root / "compatibility_rewrite_receipt.json"
    exit_receipt = receipt_root / "part2_exit_decision.json"

    move_receipt.write_text(json.dumps({
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": "UC-03",
        "part_id": "UC03-P2",
        "status": "PASS",
        "file_relocation_count": len(move_records),
        "conflict_count": len(conflicts),
        "conflict_paths": sorted(conflicts),
        "relocations": move_records,
        "semantic_merge_authority": False,
        "deletion_authority": False,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_changes = consolidate_rewrites(root_changes + path_changes)
    amendment_paths = write_upstream_amendments(repo, move_records)
    rewrite_receipt.write_text(json.dumps({
        "schema_version": "1.0.0",
        "status": "PASS",
        "modified_file_count": len({item["path"] for item in all_changes}),
        "replacement_count": sum(item["replacement_count"] for item in all_changes),
        "compatibility_shims": sorted(shims),
        "files": all_changes,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    exit_receipt.write_text(json.dumps({
        "schema_version": "1.0.0",
        "program_id": "UCPS",
        "stage_id": "UC-03",
        "part_id": "UC03-P2",
        "status": "ACCEPTED",
        "uc03_part3_authorized": True,
        "uc04_authorized": False,
        "semantic_merge_authority": False,
        "deletion_authority": False,
        "runtime_authority": False,
        "order_authority": False,
        "capital_authority": False,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    release = repo / "releases/unified_consolidation/uc03/part2"
    index = release / "PATCH_FILE_INDEX.txt"
    changed = git_changed_paths(repo)
    if changed is None:
        static = release / "STATIC_PATCH_FILE_INDEX.txt"
        paths = {
            line.strip().replace("\\", "/")
            for line in static.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        for record in move_records:
            paths.add(record["source"])
            paths.add(record["destination"])
        paths.update(item["path"] for item in all_changes)
        paths.update(shims)
        paths.update(conflicts)
        paths.update(amendment_paths)
        paths.update({
            move_receipt.relative_to(repo).as_posix(),
            rewrite_receipt.relative_to(repo).as_posix(),
            exit_receipt.relative_to(repo).as_posix(),
            index.relative_to(repo).as_posix(),
        })
    else:
        paths = set(changed)
        paths.add(index.relative_to(repo).as_posix())
    index.write_text("\n".join(sorted(paths)) + "\n", encoding="utf-8")
    refreshed = git_changed_paths(repo)
    if refreshed is not None:
        refreshed.add(index.relative_to(repo).as_posix())
        index.write_text("\n".join(sorted(refreshed)) + "\n", encoding="utf-8")
        paths = refreshed

    return {
        "status": "PASS",
        "file_relocation_count": len(move_records),
        "rewrite_file_count": len({item["path"] for item in all_changes}),
        "replacement_count": sum(item["replacement_count"] for item in all_changes),
        "compatibility_shim_count": len(shims),
        "conflict_count": len(conflicts),
        "commit_path_count": len(paths),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    arguments = parser.parse_args()
    print(json.dumps(apply(Path(arguments.repo_root)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
