"""Optional verification of the external FP source package against frozen hashes."""
from __future__ import annotations

from pathlib import Path

from .canonical import file_sha256


def parse_hash_contract(path: Path) -> dict[str, str]:
    expected: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        digest, name = line.split(None, 1)
        expected[name.strip()] = digest
    return expected


def verify_source_directory(source_root: Path, contract_path: Path) -> dict:
    expected = parse_hash_contract(contract_path)
    actual = {}
    missing = []
    mismatched = []
    for name, digest in expected.items():
        candidate = source_root / name
        if not candidate.is_file():
            missing.append(name)
            continue
        actual_digest = file_sha256(candidate)
        actual[name] = actual_digest
        if actual_digest != digest:
            mismatched.append({"name": name, "expected": digest, "actual": actual_digest})
    extra = sorted(
        path.name for path in source_root.iterdir()
        if path.is_file() and path.name not in expected
    ) if source_root.is_dir() else []
    return {
        "passed": not missing and not mismatched,
        "source_root": str(source_root),
        "expected_count": len(expected),
        "verified_count": len(actual),
        "missing": sorted(missing),
        "mismatched": mismatched,
        "extra": extra,
        "actual": actual,
    }
