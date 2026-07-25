from __future__ import annotations
from .contracts import MaturityEvidence
from .enums import OutcomeState, CensoringKind, TerminalReason

def determine_maturity(*, state:OutcomeState, terminal_reason:TerminalReason, observation_end_ms:int, required_end_ms:int, entry_time_ms:int|None, exit_time_ms:int|None) -> MaturityEvidence:
    if state==OutcomeState.RESOLVED:
        return MaturityEvidence(state,CensoringKind.NONE,observation_end_ms,required_end_ms,True,True,"",terminal_reason.value)
    if state==OutcomeState.REJECTED:
        return MaturityEvidence(state,CensoringKind.NONE,observation_end_ms,required_end_ms,True,False,"",terminal_reason.value)
    if state==OutcomeState.UNFILLED and observation_end_ms>=required_end_ms:
        return MaturityEvidence(state,CensoringKind.NONE,observation_end_ms,required_end_ms,True,False,"",terminal_reason.value)
    if state in (OutcomeState.OPEN,OutcomeState.CENSORED) and observation_end_ms>=required_end_ms:
        return MaturityEvidence(OutcomeState.CENSORED,CensoringKind.RIGHT,observation_end_ms,required_end_ms,False,False,"",terminal_reason.value)
    return MaturityEvidence(OutcomeState.UNRESOLVED,CensoringKind.UNRESOLVED,observation_end_ms,required_end_ms,False,False,"","insufficient_observation_window")
