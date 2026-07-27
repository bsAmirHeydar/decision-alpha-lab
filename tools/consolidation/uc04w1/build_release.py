from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.consolidation.ci.portable_hash import canonical_sha256
from tools.repository_paths import RepositoryPaths

RELEASE = Path("releases/unified_consolidation/uc04/w1")


def sha256(path: Path) -> str:
    return canonical_sha256(path)


def build(repo: Path) -> None:
    root = RepositoryPaths.discover(repo).root
    release = root / RELEASE
    index_path = release / "PATCH_FILE_INDEX.txt"
    paths = sorted({line.strip().replace("\\", "/") for line in index_path.read_text(encoding="utf-8").splitlines() if line.strip()})
    index_path.write_text("\n".join(paths) + "\n", encoding="utf-8", newline="\n")

    manifest_path = release / "PATCH_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["patch_file_count"] = len(paths)
    manifest["hash_ledger_entry_count"] = len(paths) - 1
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    ledger_path = release / "PATCH_FILE_HASHES.sha256"
    rows: list[str] = []
    for relative in paths:
        if relative == f"{RELEASE.as_posix()}/PATCH_FILE_HASHES.sha256":
            continue
        target = root / relative
        if not target.is_file():
            raise FileNotFoundError(relative)
        rows.append(f"{sha256(target)}  {relative}")
    ledger_path.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build UC04-W1A release hash controls.")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    build(Path(args.repo_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
