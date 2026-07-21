from pathlib import Path

import pytest

from tools.strategy_factory.lcm.lcm_13c.service import LCM13CRollbackClosureService


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@pytest.fixture(scope="session")
def built(repo_root, tmp_path_factory):
    result = LCM13CRollbackClosureService(repo_root).build(
        tmp_path_factory.mktemp("lcm13c") / "closures"
    )
    return result.output_root
