from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .errors import DestinationConflict


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def ensure_empty_destination(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise DestinationConflict(f"destination must be absent or empty: {path}")


def atomic_directory(destination: Path):
    class _AtomicDirectory:
        def __enter__(self):
            ensure_empty_destination(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            self.staging = Path(tempfile.mkdtemp(prefix=destination.name + ".staging.", dir=destination.parent))
            return self.staging

        def __exit__(self, exc_type, exc, tb):
            if exc_type is not None:
                shutil.rmtree(self.staging, ignore_errors=True)
                return False
            if destination.exists():
                destination.rmdir()
            os.replace(self.staging, destination)
            return False

    return _AtomicDirectory()
