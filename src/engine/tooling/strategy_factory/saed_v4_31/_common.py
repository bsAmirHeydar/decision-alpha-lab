from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
PY_ROOT=ROOT/"src/engine/packages"
if str(PY_ROOT) not in sys.path: sys.path.insert(0,str(PY_ROOT))
EX=ROOT/"examples/legacy/strategy_factory/saed_v4_31"
AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_31"
SC=ROOT/"schemas/legacy/strategy_factory/saed_v4_31"
DOC=ROOT/"docs/strategy_factory_sovereign_context_intelligence_v4"
MQL_INCLUDE=ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_31"
MQL_EXPERT=ROOT/"mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_31"
MAP={
"upstream":"GOLDEN_UPSTREAM_RECEIPT.JSON","model":"GOLDEN_FORMAL_MODEL.JSON","graph":"GOLDEN_REACHABILITY_GRAPH.JSON","invariants":"GOLDEN_INVARIANT_CATALOG.JSON","temporal":"GOLDEN_TEMPORAL_PROPERTY_CATALOG.JSON","invariant_report":"GOLDEN_INVARIANT_VERIFICATION_REPORT.JSON","temporal_report":"GOLDEN_BOUNDED_TEMPORAL_VERIFICATION_REPORT.JSON","mutation_scorecard":"GOLDEN_MUTATION_SCORECARD.JSON","counterexample_ledger":"GOLDEN_COUNTEREXAMPLE_LEDGER.JSON","proof_registry":"GOLDEN_PROOF_OBLIGATION_REGISTRY.JSON","proof_ledger":"GOLDEN_PROOF_DISCHARGE_LEDGER.JSON","hazards":"GOLDEN_HAZARD_REGISTER.JSON","controls":"GOLDEN_MITIGATION_CATALOG.JSON","constraints":"GOLDEN_SAFETY_CONSTRAINT_CATALOG.JSON","mitigation_coverage":"GOLDEN_MITIGATION_COVERAGE_MATRIX.JSON","residual_risk":"GOLDEN_RESIDUAL_RISK_LEDGER.JSON","assurance_case":"GOLDEN_ASSURANCE_CASE_GRAPH.JSON","claim_ledger":"GOLDEN_GSN_CLAIM_LEDGER.JSON","traceability":"GOLDEN_EVIDENCE_TRACEABILITY_MATRIX.JSON","proof_coverage":"GOLDEN_PROOF_COVERAGE_MATRIX.JSON","contract_closure":"CONTRACT_CLOSURE_REVIEW.JSON","known_time":"KNOWN_TIME_LEAKAGE_REVIEW.JSON","security":"SECURITY_REVIEW.JSON","model_risk":"MODEL_RISK_REVIEW.JSON","limitations":"FORMAL_METHOD_LIMITATIONS.JSON","reproduction":"INDEPENDENT_REPRODUCTION_RECEIPT.JSON","replay":"GOLDEN_REPLAY_RECEIPT.JSON","authority":"GOLDEN_AUTHORITY_BOUNDARY.JSON","evidence_bundle":"GOLDEN_SAFETY_CASE_EVIDENCE_BUNDLE.JSON","certificate":"GOLDEN_FORMAL_VERIFICATION_SAFETY_CASE_CERTIFICATE.JSON","handoff":"V4_31_TO_V4_32_HANDOFF.JSON"}
def load(path:Path): return json.loads(path.read_text(encoding="utf-8"))
def reference_inputs(): return load(EX/"FULL_REFERENCE_INPUT.JSON")
def reference_result():
 from saed_v4_formal_verification_safety_case.service import run
 return run(reference_inputs())
