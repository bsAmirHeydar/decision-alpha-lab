from tools.repository_paths import find_repository_root
from pathlib import Path
import pytest
@pytest.fixture(scope='session')
def repo_root():return find_repository_root(__file__)
@pytest.fixture(scope='session')
def package_root(repo_root):return repo_root/'registry/history/lcm/controlled_deletion_closures/DELETECLOSE_D38B8B1916E504C5C6F2123CF5047474'
