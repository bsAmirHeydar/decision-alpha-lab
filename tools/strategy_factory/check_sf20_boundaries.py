from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
paths=[root/"mql5/Include/AlphaLab/StrategyFactory/Integration",root/"mql5/Experts/StrategyFactory/SF20_EXP0017PilotHost.mq5",root/"mql5/Experts/StrategyFactory/SF20_EXP0017Diagnostic.mq5"]
forbidden=("OrderSend(","OrderCheck(","OrderSendAsync(","CTrade","PositionOpen(","PositionClose(","WebRequest(","live_authority=true")
text="\n".join(p.read_text(errors="ignore") for path in paths for p in ([path] if path.is_file() else path.rglob("*")) if p.is_file())
found=[x for x in forbidden if x in text]
if found: raise SystemExit("SF20 boundary failure: "+", ".join(found))
required=("sf20.exp0017.temporal_intermarket_divergence","exp0017_raw_divergence_candidate_unconfirmed_trade","NO_GOVERNED_EXP0017_MODEL","LIVE_AUTHORITY_DISABLED")
missing=[x for x in required if x not in text]
if missing: raise SystemExit("SF20 required guard missing: "+", ".join(missing))
print("SF20 boundary guard PASS")
