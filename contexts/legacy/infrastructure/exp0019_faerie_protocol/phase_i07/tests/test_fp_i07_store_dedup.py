import pytest
from dataclasses import replace
from fp_i07_confirmation import *
from fp_i07_confirmation.golden import golden_case

def test_store_deduplicates_same_pending_and_result():
    c,cfg,b,pj,p,o,r,events=golden_case();s=ConfirmationStore();assert s.admit(p,events[0]);assert not s.admit(p,events[0]);assert s.finalize(r,events[1]);assert not s.finalize(r,events[1])
def test_store_removes_pending_on_finalization():
    *_,p,o,r,events=golden_case();s=ConfirmationStore();s.admit(p,events[0]);s.finalize(r,events[1]);assert not s.pending
def test_store_exports_signal_once():
    *_,p,o,r,events=golden_case();s=ConfirmationStore();s.admit(p,events[0]);s.finalize(r,events[1]);assert len(s.signals)==1
def test_conflicting_result_rejected():
    *_,p,o,r,events=golden_case();s=ConfirmationStore();s.admit(p,events[0]);s.finalize(r,events[1]);r2=replace(r,result_hash='0'*64)
    with pytest.raises(Exception):s.finalize(r2,events[1])
