from tools.repository_paths import find_repository_root
from pathlib import Path

REPO = find_repository_root(__file__)

def test_phase_and_master_docs_are_accepted_reference():
    phase = REPO / "docs/architecture/master/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/05_PHASES/LCM_08C_CONTEXT_WAVE_MIGRATION_AND_CONTEXT_PORTFOLIO_CLOSURE.md"
    master = REPO / "docs/architecture/master/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/05_PHASES/LCM_08_CONTEXT_PACKAGE_MIGRATION.md"
    assert "status: accepted-reference" in phase.read_text()
    assert "status: accepted-reference" in master.read_text()
