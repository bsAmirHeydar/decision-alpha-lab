import pytest
from fp_i07_confirmation import *
from fp_i07_confirmation.golden import golden_case,candidate,config,host_bar

def test_hunter_only_confirms(): assert golden_case(ClosePairState.HUNTER_ONLY)[-2].outcome is ConfirmationOutcome.CONFIRMED
def test_both_invalidates(): assert golden_case(ClosePairState.BOTH)[-2].outcome is ConfirmationOutcome.INVALIDATED_DOUBLE_HUNT
def test_protected_only_role_change(): assert golden_case(ClosePairState.PROTECTED_ONLY)[-2].outcome is ConfirmationOutcome.INVALIDATED_ROLE_CHANGED
def test_none_no_signal(): assert golden_case(ClosePairState.NONE)[-2].outcome is ConfirmationOutcome.NO_SIGNAL_AT_CLOSE
def test_incomplete_unavailable(): assert golden_case(ClosePairState.DATA_INCOMPLETE)[-2].outcome is ConfirmationOutcome.UNAVAILABLE_AT_CLOSE
def test_confirmed_signal_contains_original_candidate_identity():
    c,*rest=golden_case();r=rest[-2];assert r.confirmed_signal.candidate_id==c.candidate_id
def test_confirmed_signal_direction_preserved(): assert golden_case()[-2].confirmed_signal.direction.value=='BEARISH'
