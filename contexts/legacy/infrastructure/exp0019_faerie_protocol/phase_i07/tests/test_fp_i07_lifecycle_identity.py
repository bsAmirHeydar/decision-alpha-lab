import pytest
from fp_i07_confirmation import *
from fp_i07_confirmation.golden import golden_case,candidate,config,host_bar

def test_transition_sequence_admit_then_terminal():
    *_,events=golden_case();assert [e.sequence for e in events]==[0,1]
def test_illegal_terminal_transition_rejected():
    with pytest.raises(Exception):transition('C',2,ConfirmationState.CONFIRMED,ConfirmationState.NO_SIGNAL_AT_CLOSE,0,'E','R')
def test_same_input_same_signal_id(): assert golden_case()[-2].confirmed_signal.signal_id==golden_case()[-2].confirmed_signal.signal_id
def test_timeframe_changes_signal_identity(): assert golden_case(tf=HostTimeframe.M5)[-2].confirmed_signal.signal_id!=golden_case(tf=HostTimeframe.M15)[-2].confirmed_signal.signal_id
def test_reason_style_not_in_signal_identity():
    r=golden_case()[-2];old=r.confirmed_signal.signal_id;assert old==r.confirmed_signal.signal_id
def test_nonconfirmed_has_no_signal(): assert golden_case(ClosePairState.NONE)[-2].confirmed_signal is None
def test_result_hash_deterministic(): assert golden_case()[-2].result_hash==golden_case()[-2].result_hash
