from pathlib import Path
import json
import pytest

ROOT = Path(__file__).resolve().parents[4]
FIX = ROOT / "lab" / "11_strategy_factory" / "acl_os" / "fixtures" / "acl_02"

@pytest.fixture
def valid_root():
    return FIX / "valid_context"

@pytest.fixture
def valid_permit():
    return json.loads((FIX / "valid_permit.json").read_text(encoding="utf-8"))
