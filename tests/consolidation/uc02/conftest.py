from __future__ import annotations

from pathlib import Path

import pytest

from tools.consolidation.uc02.generator import build_authority_package
from tools.consolidation.ci.verify_migration_continuity import verify as verify_migration_continuity


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@pytest.fixture(scope="session")
def reference_authority(repo_root: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    baseline = repo_root / "registry/consolidation/uc01/baselines/UC01_BASELINE_V1"
    if not baseline.is_dir():
        continuity = verify_migration_continuity(repo_root)
        if continuity.get("status") == "PASS":
            pytest.skip(
                "Historical UC-01/UC-02 dynamic packages were not committed; "
                "migration continuity is enforced by accepted UC-03 receipts and amendments."
            )
        pytest.fail(f"UC-01 baseline is absent and migration continuity failed: {continuity}")
    root = tmp_path_factory.mktemp("uc02-authority") / "UC02_AUTHORITY_V1"
    result = build_authority_package(repo_root, root, allow_reference=True)
    assert result["status"] == "PASS", result
    return root
