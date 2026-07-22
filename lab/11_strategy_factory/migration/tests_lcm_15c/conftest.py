from pathlib import Path
import pytest
@pytest.fixture(scope='session')
def repo_root():return Path(__file__).resolve().parents[4]
@pytest.fixture(scope='session')
def package_root(repo_root):return repo_root/'registry/legacy_context_migration/controlled_deletion_closures/DELETECLOSE_D38B8B1916E504C5C6F2123CF5047474'
