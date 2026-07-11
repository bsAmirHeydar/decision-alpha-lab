from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[4]
MQL=ROOT/"mql5/Include/AlphaLab/StrategyFactory/Contracts"

def test_required_headers_exist():
    required={"SF01_AllContracts.mqh","SF01_AnatomyEvent.mqh","SF01_FeatureSnapshot.mqh",
              "SF01_ArtifactIdentity.mqh","SF01_MarketTimestamp.mqh"}
    assert required.issubset({p.name for p in MQL.glob("*.mqh")})

def test_no_live_order_authority_in_phase01():
    text="\n".join(p.read_text(encoding="utf-8") for p in MQL.glob("*.mqh"))
    assert not re.search(r"\b(?:OrderSend|OrderCheck|CTrade)\s*\(?", text)

def test_all_contracts_includes_primary_types():
    text=(MQL/"SF01_AllContracts.mqh").read_text()
    for name in ("SF01_AnatomyEvent.mqh","SF01_FeatureSnapshot.mqh","SF01_ArtifactIdentity.mqh"):
        assert name in text
