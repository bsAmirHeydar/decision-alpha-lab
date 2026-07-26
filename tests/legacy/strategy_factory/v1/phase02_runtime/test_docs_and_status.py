from tools.repository_paths import find_repository_root
from pathlib import Path
import json

ROOT = find_repository_root(__file__)

def test_phase_status_accepted():
    data = json.loads((ROOT / "releases/history/strategy_factory/program/implementation/phase_status/PHASE_02.json").read_text())
    assert data["status"] == "ACCEPTED_WITH_LOCAL_MQL5_COMPILE_PENDING"

def test_roadmap_revision_has_market_services_next():
    data = json.loads((ROOT / "releases/history/strategy_factory/program/implementation/ROADMAP_REVISION_2_1_MQL5_FIRST.json").read_text())
    p3 = next(x for x in data["phases"] if x["id"] == "03")
    assert "Market Cache" in p3["name"]

def test_obsidian_moc_exists():
    assert (ROOT / "docs/history/systems/strategy_factory_implementation/phase02/00_PHASE_02_MOC.md").exists()
