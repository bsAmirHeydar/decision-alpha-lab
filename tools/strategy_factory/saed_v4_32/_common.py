from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
PY_ROOT=ROOT/"lab/11_strategy_factory/python"
if str(PY_ROOT) not in sys.path: sys.path.insert(0,str(PY_ROOT))
EX=ROOT/"lab/11_strategy_factory/examples/saed_v4_32"
AR=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_32"
SC=ROOT/"lab/11_strategy_factory/schemas/saed_v4_32"
DOC=ROOT/"docs/strategy_factory_sovereign_context_intelligence_v4"
MQL_INCLUDE=ROOT/"mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_32"
MQL_EXPERT=ROOT/"mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_32"
MAP={'upstream': 'GOLDEN_UPSTREAM_RECEIPT.JSON', 'constitution': 'GOLDEN_RESEARCH_CONSTITUTION.JSON', 'constitution_coverage': 'GOLDEN_CONSTITUTION_COVERAGE_MATRIX.JSON', 'roles': 'GOLDEN_ROLE_REGISTRY.JSON', 'agents': 'GOLDEN_AGENT_REGISTRY.JSON', 'capabilities': 'GOLDEN_CAPABILITY_MATRIX.JSON', 'separation': 'GOLDEN_SEPARATION_OF_DUTIES_MATRIX.JSON', 'tasks': 'GOLDEN_TASK_ENVELOPE_REGISTRY.JSON', 'delegation': 'GOLDEN_DELEGATION_GRAPH.JSON', 'tokens': 'GOLDEN_CAPABILITY_TOKEN_LEDGER.JSON', 'plan': 'GOLDEN_DETERMINISTIC_EXECUTION_PLAN.JSON', 'scheduler_trace': 'GOLDEN_SCHEDULER_TRACE.JSON', 'memory': 'GOLDEN_AGENT_MEMORY_BOUNDARY.JSON', 'budgets': 'GOLDEN_BUDGET_POLICY.JSON', 'budget_ledger': 'GOLDEN_BUDGET_ACCOUNTING_LEDGER.JSON', 'sources': 'GOLDEN_SOURCE_REGISTRY.JSON', 'exposure': 'GOLDEN_AGENT_EXPOSURE_LEDGER.JSON', 'prompt_ledger': 'GOLDEN_PROMPT_TASK_OUTPUT_LEDGER.JSON', 'claim_graph': 'GOLDEN_CLAIM_GRAPH.JSON', 'attribution': 'GOLDEN_SOURCE_ATTRIBUTION_MATRIX.JSON', 'contradictions': 'GOLDEN_CONTRADICTION_DISSENT_LEDGER.JSON', 'adversarial_report': 'GOLDEN_ADVERSARIAL_REPORT.JSON', 'blocking_issues': 'GOLDEN_BLOCKING_ISSUE_LEDGER.JSON', 'checkpoints': 'GOLDEN_HUMAN_REVIEW_CHECKPOINTS.JSON', 'quorum': 'GOLDEN_QUORUM_DECISION_LEDGER.JSON', 'incidents': 'GOLDEN_VIOLATION_INCIDENT_LEDGER.JSON', 'policy_ledger': 'GOLDEN_POLICY_DECISION_LEDGER.JSON', 'contract_closure': 'CONTRACT_CLOSURE_REVIEW.JSON', 'known_time': 'KNOWN_TIME_LEAKAGE_REVIEW.JSON', 'security': 'SECURITY_REVIEW.JSON', 'model_risk': 'MODEL_RISK_REVIEW.JSON', 'limitations': 'MULTI_AGENT_LIMITATIONS.JSON', 'reproduction': 'INDEPENDENT_REPRODUCTION_RECEIPT.JSON', 'replay': 'GOLDEN_REPLAY_RECEIPT.JSON', 'authority': 'GOLDEN_AUTHORITY_BOUNDARY.JSON', 'evidence_bundle': 'GOLDEN_MULTI_AGENT_EVIDENCE_BUNDLE.JSON', 'certificate': 'GOLDEN_MULTI_AGENT_RESEARCH_CONSTITUTION_CERTIFICATE.JSON', 'handoff': 'V4_32_TO_V4_33_HANDOFF.JSON'}
def load(path:Path): return json.loads(path.read_text(encoding="utf-8"))
def reference_inputs(): return load(EX/"FULL_REFERENCE_INPUT.JSON")
def reference_result():
 from saed_v4_multi_agent_research_constitution.service import run
 return run(reference_inputs())
