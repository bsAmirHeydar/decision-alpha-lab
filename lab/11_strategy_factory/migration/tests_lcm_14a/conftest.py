from pathlib import Path

import pytest

from tools.strategy_factory.lcm.lcm_14a.service import LCM14ADeprecationRedirectService


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@pytest.fixture(scope="session")
def built(repo_root, tmp_path_factory):
    result = LCM14ADeprecationRedirectService(repo_root).build(
        tmp_path_factory.mktemp("lcm14a") / "deprecation_redirects"
    )
    return result.output_root
