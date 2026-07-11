from pathlib import Path

def test_phase12_layout_and_no_live_authority():
 root=Path(__file__).resolve().parents[4]
 headers=list((root/"mql5/Include/AlphaLab/StrategyFactory/Validation").glob("*.mqh"));assert len(headers)>=9
 text="\n".join(p.read_text(encoding="utf-8") for p in headers)
 for token in ("LongToString","Order"+"Send(","Order"+"Check(","C"+"Trade"):
  assert token not in text
 assert (root/"docs/strategy_factory_implementation/phase12/00_PHASE_12_MOC.md").exists()
