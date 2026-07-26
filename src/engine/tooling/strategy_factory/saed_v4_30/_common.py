from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
PY_ROOT=ROOT/"src/engine/packages"
if str(PY_ROOT) not in sys.path: sys.path.insert(0,str(PY_ROOT))
EX=ROOT/"examples/legacy/strategy_factory/saed_v4_30"
AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_30"
SC=ROOT/"schemas/legacy/strategy_factory/saed_v4_30"
DOC=ROOT/"docs/history/systems/saed_v4"
MQL_INCLUDE=ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_30"
MQL_EXPERT=ROOT/"mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_30"
MAP={
"upstream":"GOLDEN_UPSTREAM_RECEIPT.JSON","protocol":"GOLDEN_REPLICATION_PROTOCOL.JSON","package":"GOLDEN_MULTI_LAB_PACKAGE_IDENTITY.JSON","registry":"GOLDEN_REPLICATION_LAB_REGISTRY.JSON","independence":"GOLDEN_PAIRWISE_INDEPENDENCE_MATRIX.JSON","assignments":"GOLDEN_BLINDED_ASSIGNMENT_BUNDLE.JSON","exchange":"GOLDEN_BLINDED_EXCHANGE_MANIFEST.JSON","preregistration":"GOLDEN_PREREGISTRATION_LEDGER.JSON","environments":"GOLDEN_ENVIRONMENT_ATTESTATIONS.JSON","registration_ledger":"GOLDEN_REGISTRATION_LEDGER.JSON","runs":"GOLDEN_RUN_LEDGER.JSON","results":"GOLDEN_RESULT_LEDGER.JSON","semantic":"GOLDEN_SEMANTIC_HASH_RECONCILIATION.JSON","metrics":"GOLDEN_METRIC_TOLERANCE_RECONCILIATION.JSON","disagreement":"GOLDEN_REPLICATION_DISAGREEMENT_REPORT.JSON","adjudication":"GOLDEN_ADJUDICATION_LEDGER.JSON","coverage":"GOLDEN_REPLICATION_COVERAGE_MATRIX.JSON","known_time":"KNOWN_TIME_LEAKAGE_REVIEW.JSON","security":"SECURITY_REVIEW.JSON","model_risk":"MODEL_RISK_REVIEW.JSON","replay":"GOLDEN_REPLAY_RECEIPT.JSON","authority":"GOLDEN_AUTHORITY_BOUNDARY.JSON","evidence_bundle":"GOLDEN_REPLICATION_EVIDENCE_BUNDLE.JSON","certificate":"GOLDEN_INDEPENDENT_MULTI_LAB_REPLICATION_CERTIFICATE.JSON","handoff":"V4_30_TO_V4_31_HANDOFF.JSON"}
def load(path:Path): return json.loads(path.read_text(encoding="utf-8"))
def load_example(name): return load(EX/name)
def reference_result():
 from saed_v4_independent_multi_lab_replication.service import run
 return run(load_example("FULL_REFERENCE_CONFIG.JSON"),load_example("UPSTREAM_V4_29_DOCUMENTS.JSON"),load_example("REPLICATION_PROTOCOL.JSON"),load_example("REPLICATION_PACKAGE_MANIFEST.JSON"),load_example("REPLICATION_LABS.JSON"),load_example("LAB_ENVIRONMENTS.JSON"),load_example("SYNTHETIC_REPLICATION_PAYLOAD.JSON"))
