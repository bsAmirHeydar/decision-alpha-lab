"""Canonical Alpha Lab repository path authority.

This module is intentionally dependency-light because it is imported by
production packages, migration tooling, tests, and operator scripts.  UC-04 W0
makes it the single authority for repository discovery and migration-aware path
resolution after the UC-03 physical reorganization.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

_REPOSITORY_MARKERS = (
    "README.md",
    "registry/consolidation/uc03/part3/uc04_handoff.json",
    "src/engine",
)

# Prefix fallbacks are deliberately explicit.  Exact relocation receipts are
# preferred; these rules cover operator-provided legacy paths and old tests.
_LEGACY_PREFIXES: tuple[tuple[str, str], ...] = (
    ("lab/11_strategy_factory/python/", "src/engine/packages/"),
    ("lab/11_strategy_factory/tools/", "src/engine/tooling/strategy_factory/"),
    ("tools/strategy_factory/", "src/engine/tooling/strategy_factory/"),
    ("lab/11_strategy_factory/contexts/", "contexts/legacy/strategy_factory/authored/"),
    ("lab/11_strategy_factory/generated_contexts/", "contexts/legacy/strategy_factory/generated/"),
    ("registry/strategy_factory/", "registry/history/strategy_factory/"),
    ("registry/acl_os/", "registry/history/acl/"),
    ("docs/alpha_lab_master_architecture/", "docs/architecture/master/"),
)


def _looks_like_repository(candidate: Path) -> bool:
    return all((candidate / marker).exists() for marker in _REPOSITORY_MARKERS)


def find_repository_root(start: str | Path) -> Path:
    """Return the nearest Alpha Lab repository root or fail explicitly.

    Discovery is independent of the historical ``lab/`` topology and works in
    a source archive where ``.git`` is intentionally absent.
    """

    path = Path(start).resolve()
    current = path.parent if path.is_file() else path
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "src/engine").exists():
            return candidate
        if _looks_like_repository(candidate):
            return candidate
    raise RuntimeError(f"unable to locate Alpha Lab repository root from {start}")


def _iter_source_destination_pairs(value: object) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        source = value.get("source")
        destination = value.get("destination")
        if isinstance(source, str) and isinstance(destination, str):
            yield source.replace("\\", "/"), destination.replace("\\", "/")
        for child in value.values():
            yield from _iter_source_destination_pairs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_source_destination_pairs(child)


@lru_cache(maxsize=8)
def _relocation_map(root_text: str) -> dict[str, str]:
    root = Path(root_text)
    mapping: dict[str, str] = {}
    receipt_root = root / "registry/consolidation/uc03"
    if receipt_root.is_dir():
        for path in sorted(receipt_root.rglob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for source, destination in _iter_source_destination_pairs(payload):
                mapping[source] = destination
    return mapping


def migrated_relative_path(repository_root: str | Path, relative_path: str | Path) -> str:
    """Resolve a historical repository-relative path to the accepted UC-03 path.

    The function does not require the target to exist; callers can use it while
    validating manifests and rollback records.  Resolution is bounded and
    cycle-safe.
    """

    root = find_repository_root(repository_root)
    current = Path(relative_path).as_posix().lstrip("./")
    relocation = _relocation_map(root.as_posix())
    seen: set[str] = set()
    for _ in range(8):
        if current in seen:
            raise RuntimeError(f"cyclic repository relocation detected for {relative_path}")
        seen.add(current)
        exact = relocation.get(current)
        if exact:
            current = exact
            continue
        rewritten = None
        for old, new in _LEGACY_PREFIXES:
            if current.startswith(old):
                rewritten = new + current[len(old) :]
                break
        if rewritten is None or rewritten == current:
            return current
        current = rewritten
    raise RuntimeError(f"repository relocation depth exceeded for {relative_path}")


def resolve_repository_path(
    repository_root: str | Path,
    relative_path: str | Path,
    *,
    require_exists: bool = False,
) -> Path:
    """Return a canonical absolute path for current or historical input."""

    root = find_repository_root(repository_root)
    raw = Path(relative_path)
    if raw.is_absolute():
        try:
            raw = raw.resolve().relative_to(root)
        except ValueError as exc:
            if require_exists and not raw.exists():
                raise FileNotFoundError(raw) from exc
            return raw.resolve()
    direct = root / raw
    if direct.exists():
        return direct
    resolved = root / migrated_relative_path(root, raw)
    if require_exists and not resolved.exists():
        raise FileNotFoundError(
            f"repository path is missing after UC-03 resolution: {raw.as_posix()} -> "
            f"{resolved.relative_to(root).as_posix()}"
        )
    return resolved


@dataclass(frozen=True, slots=True)
class RepositoryPaths:
    """Typed canonical topology contract for the active Alpha Lab repository."""

    root: Path

    @classmethod
    def discover(cls, start: str | Path) -> "RepositoryPaths":
        return cls(find_repository_root(start))

    @classmethod
    def from_root(cls, root: str | Path) -> "RepositoryPaths":
        return cls(find_repository_root(root))

    @property
    def source_root(self) -> Path:
        return self.root / "src/engine"

    @property
    def package_root(self) -> Path:
        return self.source_root / "packages"

    @property
    def tooling_root(self) -> Path:
        return self.source_root / "tooling"

    @property
    def context_root(self) -> Path:
        return self.root / "contexts"

    @property
    def authored_strategy_factory_context_root(self) -> Path:
        return self.context_root / "legacy/strategy_factory/authored"

    @property
    def generated_strategy_factory_context_root(self) -> Path:
        return self.context_root / "legacy/strategy_factory/generated"

    @property
    def registry_root(self) -> Path:
        return self.root / "registry"

    @property
    def historical_registry_root(self) -> Path:
        return self.registry_root / "history"

    @property
    def strategy_factory_registry_root(self) -> Path:
        return self.historical_registry_root / "strategy_factory"

    @property
    def acl_registry_root(self) -> Path:
        return self.historical_registry_root / "acl"

    @property
    def schema_root(self) -> Path:
        return self.root / "schemas"

    @property
    def release_root(self) -> Path:
        return self.root / "releases"

    @property
    def documentation_root(self) -> Path:
        return self.root / "docs/architecture/master"

    @property
    def runtime_run_root(self) -> Path:
        return self.root / ".alpha/runs"

    def authored_context(self, context_id: str) -> Path:
        return self.authored_strategy_factory_context_root / context_id

    def generated_context(self, context_slug: str) -> Path:
        return self.generated_strategy_factory_context_root / context_slug

    def resolve(self, relative_path: str | Path, *, require_exists: bool = False) -> Path:
        return resolve_repository_path(self.root, relative_path, require_exists=require_exists)
