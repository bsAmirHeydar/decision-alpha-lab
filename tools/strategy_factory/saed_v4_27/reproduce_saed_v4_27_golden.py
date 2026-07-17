from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[3]; PY=ROOT/"lab/11_strategy_factory/python"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
from saed_v4_complete_search_exposure_ledger import run
EX=ROOT/"lab/11_strategy_factory/examples/saed_v4_27"; AR=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_27"
load=lambda p: json.loads(p.read_text(encoding="utf-8"))
out=run(load(EX/"FULL_REFERENCE_CONFIG.JSON"),load(EX/"UPSTREAM_V4_26_DOCUMENTS.JSON"),load(EX/"EXPERIMENT_MANIFESTS.JSON"),load(EX/"TRIAL_EVENTS.JSON"),load(EX/"EXPOSURE_EVENTS.JSON"))
artifact_map={"GOLDEN_UPSTREAM_RECEIPT.JSON":"upstream_receipt","GOLDEN_COMPLETE_TRIAL_LEDGER.JSON":"trial_ledger","GOLDEN_COMPLETE_EXPOSURE_LEDGER.JSON":"exposure_ledger","GOLDEN_MULTIPLICITY_UNIVERSE.JSON":"multiplicity_universe","GOLDEN_COMPLETENESS_AUDIT.JSON":"completeness_audit","GOLDEN_INTEGRITY_REPORT.JSON":"integrity_report","GOLDEN_QUERY_BUDGET_SNAPSHOT.JSON":"budget_snapshot","KNOWN_TIME_LEAKAGE_REVIEW.JSON":"known_time_review","SECURITY_REVIEW.JSON":"security_review","MODEL_RISK_REVIEW.JSON":"model_risk_review","GOLDEN_AUTHORITY_BOUNDARY.JSON":"authority_boundary","GOLDEN_COMPLETE_SEARCH_EXPOSURE_CERTIFICATE.JSON":"certificate","V4_27_TO_V4_28_HANDOFF.JSON":"handoff","GOLDEN_REPLAY_RECEIPT.JSON":"replay_receipt"}
for fn,key in artifact_map.items(): assert load(AR/fn)==out[key],fn
print("V4-27 golden reproduction passed: 14 exact artifacts")
