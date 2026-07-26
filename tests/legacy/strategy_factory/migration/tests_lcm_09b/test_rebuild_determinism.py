from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from src.engine.tooling.strategy_factory.lcm.lcm_09b.canonical import file_digest
from src.engine.tooling.strategy_factory.lcm.lcm_09b.service import LCM09BSetupMigrationService

from .conftest import REPO, ROOT

_ENVIRONMENT_BOUND_FILES = frozenset(
    {
        "output_manifest.json",
        "setup_migration_receipt.json",
    }
)
_ENVIRONMENT_BOUND_KEYS = frozenset(
    {
        "absolute_path",
        "created_at",
        "generated_at",
        "generated_at_utc",
        "manifest_digest",
        "output_root",
        "package_root",
        "receipt_digest",
        "repo_root",
        "repository_root",
        "workspace_root",
    }
)


def _snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): file_digest(path)
        for path in root.rglob("*")
        if path.is_file()
    }


def _stable_snapshot(root: Path) -> dict[str, str]:
    return {
        relative: digest
        for relative, digest in _snapshot(root).items()
        if relative not in _ENVIRONMENT_BOUND_FILES
    }


def _stable_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _stable_json(item)
            for key, item in sorted(value.items())
            if key not in _ENVIRONMENT_BOUND_KEYS
        }
    if isinstance(value, list):
        return [_stable_json(item) for item in value]
    return value


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def test_clean_rebuild_is_byte_deterministic(tmp_path: Path):
    """Repeated clean builds to the same target must be byte-identical.

    The committed package may have been generated on another operating system
    or checkout root. Core generated artifacts must still match byte-for-byte;
    publication wrappers are compared semantically after removing explicitly
    environment-bound metadata.
    """

    output = tmp_path / "migration"
    service = LCM09BSetupMigrationService()

    service.build(REPO, output)
    first = _snapshot(output)

    shutil.rmtree(output)
    service.build(REPO, output)
    second = _snapshot(output)

    assert first == second
    assert _stable_snapshot(ROOT) == _stable_snapshot(output)

    for relative in sorted(_ENVIRONMENT_BOUND_FILES):
        assert _stable_json(_load_json(ROOT / relative)) == _stable_json(
            _load_json(output / relative)
        )
