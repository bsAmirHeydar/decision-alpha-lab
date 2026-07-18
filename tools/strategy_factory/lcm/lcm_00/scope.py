from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .canonical import digest_object, normalize_root_relative

DEFAULT_EXCLUDED_DIR_NAMES = (
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
)
DEFAULT_EXCLUDED_FILE_GLOBS = (
    "*.pyc",
    "*.pyo",
    "*.tmp",
    "*.temp",
    "*.lock",
    ".DS_Store",
    "Thumbs.db",
)


@dataclass(frozen=True)
class ScopePolicy:
    policy_id: str
    version: str
    included_roots: tuple[str, ...] = (".",)
    excluded_dir_names: tuple[str, ...] = DEFAULT_EXCLUDED_DIR_NAMES
    excluded_file_globs: tuple[str, ...] = DEFAULT_EXCLUDED_FILE_GLOBS
    include_symlinks_as_records: bool = True
    follow_symlinks: bool = False

    def to_dict(self) -> dict:
        value = {
            "schema_version": "1.0.0",
            "policy_id": self.policy_id,
            "version": self.version,
            "included_roots": list(self.included_roots),
            "excluded_dir_names": list(self.excluded_dir_names),
            "excluded_file_globs": list(self.excluded_file_globs),
            "include_symlinks_as_records": self.include_symlinks_as_records,
            "follow_symlinks": self.follow_symlinks,
            "path_semantics": "ROOT_RELATIVE_POSIX_BYTE_EXACT",
            "scope_policy_digest": "",
        }
        value["scope_policy_digest"] = digest_object(value, "scope_policy_digest")
        return value


def classify_path(rel: str, policy: ScopePolicy) -> tuple[bool, str]:
    rel = normalize_root_relative(rel)
    parts = Path(rel).parts
    for part in parts[:-1]:
        if part in policy.excluded_dir_names:
            return False, f"EXCLUDED_DIRECTORY:{part}"
    name = parts[-1]
    for pattern in policy.excluded_file_globs:
        if fnmatch.fnmatch(name, pattern):
            return False, f"EXCLUDED_FILE_PATTERN:{pattern}"
    return True, "IN_SCOPE"
