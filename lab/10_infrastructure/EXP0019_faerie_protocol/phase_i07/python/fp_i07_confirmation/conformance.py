from .enums import ClosePairState,ConfirmationOutcome
from .golden import golden_case
CASES={ClosePairState.HUNTER_ONLY:ConfirmationOutcome.CONFIRMED,ClosePairState.BOTH:ConfirmationOutcome.INVALIDATED_DOUBLE_HUNT,ClosePairState.PROTECTED_ONLY:ConfirmationOutcome.INVALIDATED_ROLE_CHANGED,ClosePairState.NONE:ConfirmationOutcome.NO_SIGNAL_AT_CLOSE,ClosePairState.DATA_INCOMPLETE:ConfirmationOutcome.UNAVAILABLE_AT_CLOSE}
def run_conformance():
    out=[]
    for state,expected in CASES.items():
        *_,result,_=golden_case(state)
        out.append((state.value,result.outcome.value,result.outcome is expected))
    return tuple(out)
