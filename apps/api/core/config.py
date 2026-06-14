from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "lab").exists() and (parent / "docs").exists():
            return parent
    return here.parents[3]


@dataclass(frozen=True)
class Settings:
    root_path: Path = find_repo_root()
    api_title: str = "Decision Alpha Lab API"
    api_version: str = "0.3.0"


settings = Settings()
