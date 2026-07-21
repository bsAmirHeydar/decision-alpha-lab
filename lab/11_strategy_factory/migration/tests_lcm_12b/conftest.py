from pathlib import Path
import pytest
@pytest.fixture
def repo_root():
    return Path(__file__).resolve().parents[4]
@pytest.fixture
def reconciliation_root(repo_root):
    roots = sorted((repo_root / "registry/legacy_context_migration/documentation_reconciliations").glob("DOCRECON_*"))
    assert roots
    return roots[-1]
