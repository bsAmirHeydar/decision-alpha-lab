from tools.repository_paths import find_repository_root
from pathlib import Path

import pytest

from tools.strategy_factory.lcm.lcm_13c.service import LCM13CRollbackClosureService


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return find_repository_root(__file__)


@pytest.fixture(scope="session")
def built(repo_root, tmp_path_factory):
    result = LCM13CRollbackClosureService(repo_root).build(
        tmp_path_factory.mktemp("lcm13c") / "closures"
    )
    return result.output_root
