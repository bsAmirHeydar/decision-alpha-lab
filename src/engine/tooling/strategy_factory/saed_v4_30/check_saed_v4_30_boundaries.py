from __future__ import annotations
import re,json
from _common import ROOT,AR
pkg=ROOT/"src/engine/packages/saed_v4_independent_multi_lab_replication"
forbidden=[r"\bMetaTrader5\b",r"\border_send\s*\(",r"\bOrderSend\s*\(",r"\bCTrade\b",r"\bTRADE_ACTION_DEAL\b"]
for path in pkg.glob("*.py"):
 text=path.read_text(encoding="utf-8")
 for pattern in forbidden:
  if re.search(pattern,text): raise AssertionError(f"execution boundary violation {pattern} in {path}")
cert=json.loads((AR/"GOLDEN_INDEPENDENT_MULTI_LAB_REPLICATION_CERTIFICATE.JSON").read_text())
auth=json.loads((AR/"GOLDEN_AUTHORITY_BOUNDARY.JSON").read_text())
assert not any(auth["authority"].values())
for key in ["real_external_lab_independence_claim","external_institutional_replication_claim","external_signature_claim","physical_separation_claim","real_alpha_claim","prospective_success_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","live_trading_authority"]: assert cert[key] is False,key
print("V4-30 authority and execution boundary validation passed")
