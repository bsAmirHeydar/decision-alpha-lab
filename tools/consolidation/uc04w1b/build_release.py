from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from tools.repository_paths import RepositoryPaths
from tools.consolidation.uc04w1b.contracts import RELEASE_ROOT
from tools.consolidation.uc04w1b.package_validation import (
    LEDGER_RELATIVE,
    MANIFEST_RELATIVE,
    PackageValidationError,
    verify_tree,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _index_rows(root: Path, index_path: Path) -> list[str]:
    rows = sorted(
        {
            line.strip().replace("\\", "/")
            for line in index_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    )
    if not rows:
        raise ValueError("PATCH_FILE_INDEX.txt is empty")
    for relative in rows:
        if not (root / relative).is_file():
            raise FileNotFoundError(relative)
    return rows


def _expected_files(root: Path) -> tuple[str, str, str]:
    release = root / RELEASE_ROOT
    index_path = release / "PATCH_FILE_INDEX.txt"
    manifest_path = release / "PATCH_MANIFEST.json"
    ledger_path = release / "PATCH_FILE_HASHES.sha256"

    rows = _index_rows(root, index_path)
    index_text = "\n".join(rows) + "\n"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["patch_file_count"] = len(rows)
    manifest["hash_ledger_entry_count"] = len(rows) - 1
    manifest["payload_total_bytes_excluding_manifest_and_hash_ledger"] = sum(
        (root / relative).stat().st_size
        for relative in rows
        if relative not in {MANIFEST_RELATIVE.as_posix(), LEDGER_RELATIVE.as_posix()}
    )
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"

    # The manifest hash must be calculated from the expected manifest bytes, not
    # from the possibly stale file on disk.
    ledger_rows: list[str] = []
    ledger_relative = LEDGER_RELATIVE.as_posix()
    manifest_relative = MANIFEST_RELATIVE.as_posix()
    for relative in rows:
        if relative == ledger_relative:
            continue
        if relative == manifest_relative:
            digest = hashlib.sha256(manifest_text.encode("utf-8")).hexdigest()
        elif relative == (RELEASE_ROOT / "PATCH_FILE_INDEX.txt").as_posix():
            digest = hashlib.sha256(index_text.encode("utf-8")).hexdigest()
        else:
            digest = sha256(root / relative)
        ledger_rows.append(f"{digest}  {relative}")
    ledger_text = "\n".join(ledger_rows) + "\n"
    return index_text, manifest_text, ledger_text


def build(repo: Path, *, check: bool = False) -> None:
    root = RepositoryPaths.discover(repo).root
    release = root / RELEASE_ROOT
    index_text, manifest_text, ledger_text = _expected_files(root)
    expected = {
        release / "PATCH_FILE_INDEX.txt": index_text,
        release / "PATCH_MANIFEST.json": manifest_text,
        release / "PATCH_FILE_HASHES.sha256": ledger_text,
    }

    if check:
        mismatches = [
            path.relative_to(root).as_posix()
            for path, text in expected.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != text
        ]
        if mismatches:
            raise PackageValidationError(
                "release controls are stale; run build_release without --check: " + ", ".join(mismatches)
            )
    else:
        for path, text in expected.items():
            path.write_text(text, encoding="utf-8", newline="\n")

    verify_tree(root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or verify UC04-W1B-Q release controls.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        build(Path(args.repo_root), check=args.check)
    except (OSError, ValueError, PackageValidationError) as exc:
        print(f"UC04-W1B-Q release build failed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
