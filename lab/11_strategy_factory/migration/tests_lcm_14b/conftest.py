from pathlib import Path
import json
import pytest
ROOT=Path(__file__).resolve().parents[4]
QROOT=ROOT/'registry/legacy_context_migration/quarantine_observations/QUARANTINE_F2B27A6A93EB63C1B264B84DAFA00C2D'
@pytest.fixture(scope="session")
def qroot(): return QROOT
@pytest.fixture(scope="session")
def load(): return lambda name: json.loads((QROOT/name).read_text(encoding="utf-8"))
