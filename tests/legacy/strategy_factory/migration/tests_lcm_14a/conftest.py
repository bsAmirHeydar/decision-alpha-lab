from tools.repository_paths import find_repository_root
from pathlib import Path

import pytest

from src.engine.tooling.strategy_factory.lcm.lcm_14a.service import LCM14ADeprecationRedirectService


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return find_repository_root(__file__)


@pytest.fixture(scope="session")
def built(repo_root, tmp_path_factory):
    result = LCM14ADeprecationRedirectService(repo_root).build(
        tmp_path_factory.mktemp("lcm14a") / "deprecation_redirects"
    )
    return result.output_root
