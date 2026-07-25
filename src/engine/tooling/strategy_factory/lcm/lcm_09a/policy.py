from __future__ import annotations
FORBIDDEN_AUTHORITY=("runtime_authority_created","live_order_authority_created","capital_authority_created")
def validate_contract_boundary(c:dict)->list[str]:
    failures=[]
    a=c["authority_boundary"]
    if a["broker_state_in_canonical_contract"]: failures.append("BROKER_STATE_EMBEDDED")
    if a["drawing_state_in_canonical_contract"]: failures.append("DRAWING_STATE_EMBEDDED")
    if a["execution_quota_in_canonical_contract"]: failures.append("QUOTA_EMBEDDED")
    if c["implementation_authorized"] and c["blocking_reasons"]: failures.append("BLOCKED_IMPLEMENTATION_AUTHORIZED")
    return failures
