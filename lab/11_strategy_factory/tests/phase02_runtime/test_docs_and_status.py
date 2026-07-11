from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[4]

def test_phase_status_accepted():
    data = json.loads((ROOT / "lab/11_strategy_factory/implementation_program/phase_status/PHASE_02.json").read_text())
    assert data["status"] == "ACCEPTED_WITH_LOCAL_MQL5_COMPILE_PENDING"

def test_roadmap_revision_has_market_services_next():
    data = json.loads((ROOT / "lab/11_strategy_factory/implementation_program/ROADMAP_REVISION_2_1_MQL5_FIRST.json").read_text())
    p3 = next(x for x in data["phases"] if x["id"] == "03")
    assert "Market Cache" in p3["name"]

def test_obsidian_moc_exists():
    assert (ROOT / "docs/strategy_factory_implementation/phase02/00_PHASE_02_MOC.md").exists()
