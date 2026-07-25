from __future__ import annotations
from .canonical import digest_object,with_digest
from .errors import PolicyError
PARITY_REQUIREMENTS=[
 ('SOURCE_PROMOTION_PACKAGE_INTEGRITY','PACKAGE','HARD'),('RUNTIME_CANDIDATE_PRESENT','ELIGIBILITY','HARD'),
 ('IMMUTABLE_GENERATION_INPUTS','GENERATION','HARD'),('REFERENCE_EXECUTOR_VECTOR_SET','PARITY','HARD'),
 ('MQL5_COMPILE_EVIDENCE','PARITY','HARD'),('STRATEGY_TESTER_GOLDEN_REPLAY','PARITY','HARD'),
 ('DECISION_PARITY','PARITY','HARD'),('STATE_TRANSITION_PARITY','PARITY','HARD'),('TREATMENT_PARITY','PARITY','HARD'),
 ('EXECUTION_ECONOMICS_PARITY','ECONOMICS','HARD'),('BROKER_SYMBOL_QUALIFICATION','ENVIRONMENT','HARD'),
 ('TIMEZONE_AND_SESSION_PARITY','ENVIRONMENT','HARD'),('NUMERIC_TOLERANCE_POLICY','PARITY','HARD'),
 ('SIGNED_GENERATION_ENVELOPE','CUSTODY','HARD'),('SIGNING_KEY_CUSTODY','CUSTODY','HARD'),
 ('REVOCATION_AND_ROLLBACK_PLAN','CUSTODY','HARD'),('TRUSTED_COMPUTING_BASE','SECURITY','HARD'),
 ('RUNTIME_MONITORING_CONTRACT','OPERATIONS','HARD'),('FAIL_CLOSED_FALLBACK','OPERATIONS','HARD'),
 ('ACTIVATION_AUTHORITY','AUTHORITY','HARD')]
CUSTODY_STATES=['NO_RUNTIME_CANDIDATES','PARITY_ASSESSMENT_BLOCKED','PARITY_INCOMPLETE','READY_FOR_SIGNED_BUILD_NOT_AUTHORIZED']
def parity_registry() -> dict:
    items=[]
    for rid,cat,sev in PARITY_REQUIREMENTS:
        body={'requirement_id':rid,'version':'1.0.0','category':cat,'severity':sev,'unknown_blocks_runtime':True}
        items.append({**body,'requirement_digest':digest_object(body)})
    return with_digest({'schema_version':'1.0.0','closed':True,'dynamic_registration_allowed':False,'requirements':items},'registry_digest')
def custody_state_registry() -> dict:
    items=[]
    for state in CUSTODY_STATES:
        body={'state_id':state,'version':'1.0.0','runtime_executable':False,'live_order_allowed':False,'capital_allowed':False}
        items.append({**body,'state_digest':digest_object(body)})
    return with_digest({'schema_version':'1.0.0','closed':True,'states':items},'registry_digest')
def validate_registry(r: dict,kind: str) -> None:
    if r.get('closed') is not True: raise PolicyError(f'ACL11_{kind}_REGISTRY_OPEN')
