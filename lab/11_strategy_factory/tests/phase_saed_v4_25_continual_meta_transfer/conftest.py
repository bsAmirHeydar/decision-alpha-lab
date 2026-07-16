from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
PYTHON_ROOT = ROOT / "lab/11_strategy_factory/python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

EXAMPLES = ROOT / "lab/11_strategy_factory/examples/saed_v4_25"
ARTIFACTS = ROOT / "lab/11_strategy_factory/artifacts/saed_v4_25"
SCHEMAS = ROOT / "lab/11_strategy_factory/schemas/saed_v4_25"


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
