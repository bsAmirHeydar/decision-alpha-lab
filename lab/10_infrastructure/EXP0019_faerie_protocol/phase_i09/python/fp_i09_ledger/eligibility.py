from fp_i08_weekly.enums import GateEligibility
from .enums import EligibilityOutcome,PrecheckState

def evaluate_eligibility(e):
    if not e.relation_enabled: return EligibilityOutcome.BLOCKED_RELATION_DISABLED
    if not e.data_ready: return EligibilityOutcome.BLOCKED_DATA
    if e.precheck_state is PrecheckState.BLOCKED: return EligibilityOutcome.BLOCKED_PRECHECK
    if e.gate_eligibility is GateEligibility.SUPPRESSED: return EligibilityOutcome.SUPPRESSED_BY_WW
    if e.gate_eligibility is GateEligibility.BLOCKED: return EligibilityOutcome.BLOCKED_DATA
    return EligibilityOutcome.ELIGIBLE
