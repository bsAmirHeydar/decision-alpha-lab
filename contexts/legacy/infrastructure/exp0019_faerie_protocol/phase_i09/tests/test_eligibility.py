from fp_i08_weekly.enums import GateEligibility
from fp_i09_ledger.eligibility import evaluate_eligibility
from fp_i09_ledger.enums import EligibilityOutcome,PrecheckState
from conftest import signal,gate,eligible

def test_allowed_is_eligible():
    s=signal(); assert evaluate_eligibility(eligible(s)) is EligibilityOutcome.ELIGIBLE
def test_ww_suppression_retained():
    s=signal(); g=gate(s,GateEligibility.SUPPRESSED); e=eligible(s,g); assert evaluate_eligibility(e) is EligibilityOutcome.SUPPRESSED_BY_WW
def test_blocked_gate_blocks_data():
    s=signal(); g=gate(s,GateEligibility.BLOCKED); assert evaluate_eligibility(eligible(s,g)) is EligibilityOutcome.BLOCKED_DATA
def test_relation_disabled():
    s=signal(); assert evaluate_eligibility(eligible(s,relation_enabled=False)) is EligibilityOutcome.BLOCKED_RELATION_DISABLED
def test_data_not_ready():
    s=signal(); assert evaluate_eligibility(eligible(s,data_ready=False)) is EligibilityOutcome.BLOCKED_DATA
def test_precheck_blocked():
    s=signal(); assert evaluate_eligibility(eligible(s,precheck_state=PrecheckState.BLOCKED)) is EligibilityOutcome.BLOCKED_PRECHECK
