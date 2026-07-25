"""Deterministic repository scanners for FP-I00."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable
import csv
import json
import re

from .canonical import aggregate_files_hash, file_sha256
from .models import DependencyRecord, TestRecord, OwnershipRecord


TEXT_SUFFIXES = {".mqh", ".mq5", ".py", ".ps1", ".md", ".json", ".csv", ".ini", ".set"}
FORBIDDEN_RUNTIME_TOKENS = (
    "Order" + "Send(", "C" + "Trade", "Position" + "Open(", "B" + "uy(", "S" + "ell(",
    "Web" + "Request(", "Socket" + "Create(", "Shell" + "Execute", "subprocess." + "Popen",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_files(root: Path, relative_root: str, suffixes: Iterable[str] | None = None) -> list[Path]:
    base = root / relative_root
    if not base.exists():
        return []
    allowed = set(suffixes or ())
    files = []
    for path in base.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if allowed and path.suffix not in allowed:
            continue
        files.append(path)
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def component_version(files: list[Path]) -> str:
    patterns = (
        re.compile(r"#define\s+[A-Z0-9_]+_MAJOR\s+(\d+)"),
        re.compile(r"#define\s+[A-Z0-9_]+_MINOR\s+(\d+)"),
        re.compile(r"#define\s+[A-Z0-9_]+_PATCH\s+(\d+)"),
    )
    values: list[int] = []
    for path in files:
        if path.suffix not in {".mqh", ".mq5", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        found = []
        for pattern in patterns:
            match = pattern.search(text)
            found.append(int(match.group(1)) if match else None)
        if all(value is not None for value in found):
            return ".".join(str(value) for value in found)
    return "HASH_PINNED"


def scan_dependencies(repo: Path, policy: dict) -> list[DependencyRecord]:
    records = []
    for item in policy["shared_dependencies"]:
        if item.get("globs"):
            base = repo / item["relative_root"]
            selected = set()
            for pattern in item["globs"]:
                selected.update(path for path in base.glob(pattern) if path.is_file())
            files = sorted(selected, key=lambda path: path.relative_to(repo).as_posix())
        else:
            files = collect_files(repo, item["relative_root"], item.get("suffixes"))
        records.append(DependencyRecord(
            dependency_id=item["dependency_id"],
            semantic_owner=item["semantic_owner"],
            reuse_classification=item["reuse_classification"],
            relative_root=item["relative_root"],
            file_count=len(files),
            aggregate_sha256=aggregate_files_hash(repo, files) if files else "",
            exact_version=component_version(files),
            required_for_phase=item["required_for_phase"],
            mutation_allowed=bool(item["mutation_allowed"]),
        ))
    return records


def scan_tests(repo: Path, policy: dict) -> list[TestRecord]:
    return [
        TestRecord(
            context_id=item["context_id"],
            test_id=item["test_id"],
            test_type=item["test_type"],
            relative_path=item["relative_path"],
            exists=(repo / item["relative_path"]).is_file(),
            compile_required=bool(item["compile_required"]),
            execution_command=item["execution_command"],
        )
        for item in policy["previous_context_tests"]
    ]


def scan_ownership(policy: dict) -> list[OwnershipRecord]:
    return [OwnershipRecord(**item) for item in policy["phase_ownership"]]


def scan_forbidden_authority(repo: Path, relative_roots: Iterable[str]) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    for relative_root in relative_roots:
        for path in collect_files(repo, relative_root):
            if path.suffix not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in FORBIDDEN_RUNTIME_TOKENS:
                if token in text:
                    hits.append((path.relative_to(repo).as_posix(), token))
    return hits


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
