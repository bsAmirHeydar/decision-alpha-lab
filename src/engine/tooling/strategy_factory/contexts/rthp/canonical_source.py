from __future__ import annotations

import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

TEXT_EXTENSIONS = frozenset(
    {
        ".bat",
        ".cmd",
        ".conf",
        ".csv",
        ".html",
        ".ini",
        ".json",
        ".md",
        ".ps1",
        ".py",
        ".toml",
        ".txt",
        ".xml",
        ".yaml",
        ".yml",
    }
)


def _canonical_payload(path: Path) -> bytes:
    raw = path.read_bytes()
    if path.suffix.casefold() not in TEXT_EXTENSIONS:
        return raw
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


@contextmanager
def canonical_context_mirror(package_root: Path) -> Iterator[Path]:
    """Yield an LF-canonical mirror without mutating the approved Context.

    ACL-03 approvals are byte-bound. Git checkouts on Windows can expose an
    otherwise identical text source with CRLF bytes. The RTHP adapter compiles
    an ephemeral LF mirror, allowing the central compiler to keep its strict
    raw-byte approval semantics. Any semantic byte change remains a blocker.
    """

    source_root = package_root.resolve()
    if not source_root.is_dir():
        raise FileNotFoundError(source_root)

    with tempfile.TemporaryDirectory(prefix="rthp_acl03_canonical_source_") as temporary:
        mirror = Path(temporary) / source_root.name
        mirror.mkdir(parents=True)
        for source in sorted(source_root.rglob("*")):
            if source.is_symlink():
                raise ValueError(f"symlink is forbidden in RTHP Context source: {source}")
            relative = source.relative_to(source_root)
            target = mirror / relative
            if source.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if not source.is_file():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix.casefold() in TEXT_EXTENSIONS:
                target.write_bytes(_canonical_payload(source))
            else:
                shutil.copy2(source, target)
        yield mirror
