from __future__ import annotations

from pathlib import Path

import pytest

from tools.consolidation.uc02.generator import build_authority_package


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@pytest.fixture(scope="session")
def reference_authority(repo_root: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("uc02-authority") / "UC02_AUTHORITY_V1"
    result = build_authority_package(repo_root, root, allow_reference=True)
    assert result["status"] == "PASS", result
    return root
