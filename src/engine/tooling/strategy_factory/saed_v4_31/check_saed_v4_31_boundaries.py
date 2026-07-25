from __future__ import annotations
import json,re
from _common import ROOT,AR
pkg=ROOT/"src/engine/packages/saed_v4_formal_verification_safety_case"
forbidden=[r"MetaTrader5",r"order_send\s*\(",r"OrderSend\s*\(",r"CTrade",r"TRADE_ACTION_DEAL",r"requests\.",r"socket\.",r"subprocess\."]
for path in pkg.glob("*.py"):
 text=path.read_text(encoding="utf-8")
 for pattern in forbidden:
  if re.search(pattern,text): raise AssertionError(f"boundary violation {pattern} in {path}")
auth=json.loads((AR/"GOLDEN_AUTHORITY_BOUNDARY.JSON").read_text()); cert=json.loads((AR/"GOLDEN_FORMAL_VERIFICATION_SAFETY_CASE_CERTIFICATE.JSON").read_text())
assert not any(auth["authority"].values())
for key in ["promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","live_trading_authority"]: assert cert[key] is False
print("V4-31 authority and execution boundary validation passed")
