import pytest

from fp_i02_kernel.enums import CandidateState, QuotaConsumptionPolicy, QuotaState, ReferenceState, WWState
from fp_i02_kernel.errors import FPI02Error
from fp_i02_kernel.lifecycle import CANDIDATE_MACHINE, QUOTA_MACHINE, REFERENCE_MACHINE, WW_MACHINE


def test_candidate_happy_path():
    observed = CANDIDATE_MACHINE.transition("c", CandidateState.OBSERVED, CandidateState.RAW_CANDIDATE, "e1", 1, "FP_RC_READY")
    confirmed = CANDIDATE_MACHINE.transition("c", CandidateState.RAW_CANDIDATE, CandidateState.CONFIRMED, "e2", 2, "FP_RC_CONFIRMED_ACTIVE")
    assert observed.next_state is CandidateState.RAW_CANDIDATE
    assert confirmed.next_state is CandidateState.CONFIRMED


def test_candidate_terminal_state_cannot_reopen():
    with pytest.raises(FPI02Error) as exc:
        CANDIDATE_MACHINE.transition("c", CandidateState.CONFIRMED, CandidateState.RAW_CANDIDATE, "e", 3, "FP_RC_READY")
    assert exc.value.code == "FP_RC_ILLEGAL_TRANSITION"


def test_hunter_seen_does_not_consume_reference():
    event = REFERENCE_MACHINE.transition("r", ReferenceState.FRESH, ReferenceState.HUNTER_SEEN, "h", 1, "FP_RC_READY")
    assert event.next_state is ReferenceState.HUNTER_SEEN
    assert REFERENCE_MACHINE.can_transition(ReferenceState.HUNTER_SEEN, ReferenceState.CONSUMED_BY_PROTECTED_TOUCH)


def test_ww_can_neutralize_but_not_reconfirm():
    assert WW_MACHINE.can_transition(WWState.CONFIRMED, WWState.NEUTRALIZED)
    assert not WW_MACHINE.can_transition(WWState.NEUTRALIZED, WWState.CONFIRMED)


def test_quota_consumption_fails_while_policy_unset():
    with pytest.raises(FPI02Error) as exc:
        QUOTA_MACHINE.transition("q", QuotaState.RESERVED, QuotaState.CONSUMED, "e", 1, "FP_RC_READY", QuotaConsumptionPolicy.UNSET)
    assert exc.value.code == "FP_RC_OPEN_DECISION_BLOCKS_LIVE"


def test_quota_consumption_is_structurally_possible_after_policy_freeze():
    event = QUOTA_MACHINE.transition("q", QuotaState.RESERVED, QuotaState.CONSUMED, "e", 1, "FP_RC_READY", QuotaConsumptionPolicy.FILLED)
    assert event.next_state is QuotaState.CONSUMED
