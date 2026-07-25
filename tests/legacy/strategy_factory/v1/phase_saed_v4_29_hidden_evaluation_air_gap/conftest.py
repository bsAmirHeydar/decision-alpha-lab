from tools.repository_paths import find_repository_root
import json
import sys
from pathlib import Path
import pytest

ROOT = find_repository_root(__file__)
PY_ROOT = ROOT / "src/engine/packages"
if str(PY_ROOT) not in sys.path:
    sys.path.insert(0, str(PY_ROOT))
EX = ROOT / "examples/legacy/strategy_factory/saed_v4_29"


def load(name):
    return json.loads((EX / name).read_text(encoding="utf-8"))


@pytest.fixture
def config():
    return load("FULL_REFERENCE_CONFIG.JSON")


@pytest.fixture
def upstream():
    return load("UPSTREAM_V4_28_DOCUMENTS.JSON")


@pytest.fixture
def manifest():
    return load("PROTECTED_CUSTODY_MANIFEST.JSON")


@pytest.fixture
def candidate():
    return load("CANDIDATE_SUBMISSION.JSON")


@pytest.fixture
def fixture():
    return load("SEALED_SYNTHETIC_EVALUATION_FIXTURE.JSON")


@pytest.fixture
def result(config, upstream, manifest, candidate, fixture):
    from saed_v4_hidden_evaluation_air_gap.service import run

    return run(config, upstream, manifest, candidate, fixture)
