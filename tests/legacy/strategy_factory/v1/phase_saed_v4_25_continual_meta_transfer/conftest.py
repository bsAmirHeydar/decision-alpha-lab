from __future__ import annotations
from tools.repository_paths import find_repository_root

import json
import sys
from pathlib import Path

import pytest

ROOT = find_repository_root(__file__)
PYTHON_ROOT = ROOT / "src/engine/packages"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

EXAMPLES = ROOT / "examples/legacy/strategy_factory/saed_v4_25"
ARTIFACTS = ROOT / "releases/history/strategy_factory/artifacts/saed_v4_25"
SCHEMAS = ROOT / "schemas/legacy/strategy_factory/saed_v4_25"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def config():
    return load(EXAMPLES / "FULL_REFERENCE_CONFIG.JSON")


@pytest.fixture(scope="session")
def upstream():
    return load(EXAMPLES / "UPSTREAM_V4_24_DOCUMENTS.JSON")


@pytest.fixture(scope="session")
def tasks():
    return load(EXAMPLES / "META_TASK_RECORDS.JSON")


@pytest.fixture(scope="session")
def golden_outputs():
    mapping = {}
    for path in ARTIFACTS.glob("*.JSON"):
        mapping[path.name] = load(path)
    return mapping
