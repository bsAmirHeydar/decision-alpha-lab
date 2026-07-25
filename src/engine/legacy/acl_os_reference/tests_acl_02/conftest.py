from tools.repository_paths import find_repository_root
from pathlib import Path
import json
import pytest

ROOT = find_repository_root(__file__)
FIX = ROOT / "lab" / "11_strategy_factory" / "acl_os" / "fixtures" / "acl_02"

@pytest.fixture
def valid_root():
    return FIX / "valid_context"

@pytest.fixture
def valid_permit():
    return json.loads((FIX / "valid_permit.json").read_text(encoding="utf-8"))
