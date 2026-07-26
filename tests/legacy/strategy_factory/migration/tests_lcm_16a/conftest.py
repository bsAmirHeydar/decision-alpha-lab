from __future__ import annotations
from tools.repository_paths import find_repository_root

import json
from pathlib import Path

import pytest

ROOT = find_repository_root(__file__)
AUDIT_ROOT = ROOT / "registry/history/lcm/full_system_audits/CLOSUREAUDIT_5EEC97304039BFF3AAAFB57605961BA2"
SCHEMA_ROOT = ROOT / "registry/history/lcm/lcm_16a/schemas/v1"
MODULE_ROOT = ROOT / "src/engine/tooling/strategy_factory/lcm/lcm_16a"


@pytest.fixture
def root() -> Path:
    return ROOT


@pytest.fixture
def audit_root() -> Path:
    return AUDIT_ROOT


@pytest.fixture
def load(audit_root):
    def _load(relative: str):
        return json.loads((audit_root / relative).read_text(encoding="utf-8-sig"))
    return _load
