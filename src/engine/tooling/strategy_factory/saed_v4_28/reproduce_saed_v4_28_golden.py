from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__); PY=ROOT/"src/engine/packages"
if str(PY) not in sys.path: sys.path.insert(0,str(PY))
from saed_v4_anytime_valid_online_fdr import run
EX=ROOT/"examples/legacy/strategy_factory/saed_v4_28"; AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_28"
load=lambda p:json.loads(p.read_text(encoding="utf-8")); out=run(load(EX/"FULL_REFERENCE_CONFIG.JSON"),load(EX/"UPSTREAM_V4_27_DOCUMENTS.JSON"),load(EX/"HYPOTHESIS_STREAM.JSON"))
M={"upstream_receipt":"GOLDEN_UPSTREAM_RECEIPT.JSON","anytime_evidence_registry":"GOLDEN_ANYTIME_EVIDENCE_REGISTRY.JSON","family_allocation":"GOLDEN_FAMILY_ALLOCATION.JSON","wealth_ledger":"GOLDEN_ONLINE_FDR_WEALTH_LEDGER.JSON","rejection_ledger":"GOLDEN_REJECTION_LEDGER.JSON","stopping_rule_audit":"GOLDEN_STOPPING_RULE_AUDIT.JSON","online_fdr_audit":"GOLDEN_ONLINE_FDR_AUDIT.JSON","challenger_comparison":"GOLDEN_CHALLENGER_COMPARISON.JSON","known_time_review":"KNOWN_TIME_LEAKAGE_REVIEW.JSON","security_review":"SECURITY_REVIEW.JSON","model_risk_review":"MODEL_RISK_REVIEW.JSON","authority_boundary":"GOLDEN_AUTHORITY_BOUNDARY.JSON","certificate":"GOLDEN_ANYTIME_VALID_ONLINE_FDR_CERTIFICATE.JSON","handoff":"V4_28_TO_V4_29_HANDOFF.JSON","replay_receipt":"GOLDEN_REPLAY_RECEIPT.JSON"}
for k,n in M.items(): assert out[k]==load(AR/n),k
print(f"V4-28 golden reproduction passed: {len(M)} exact artifacts")
