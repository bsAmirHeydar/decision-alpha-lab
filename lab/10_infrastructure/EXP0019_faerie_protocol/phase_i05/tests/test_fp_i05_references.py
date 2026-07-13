import pytest
from dataclasses import replace
from fp_i02_kernel.enums import ReferenceState,PriceSide
from fp_i05_reference.golden import golden_completed_n_window
from fp_i05_reference.reference_engine import derive_reference_set,transition_reference
from fp_i05_reference.enums import ReferenceTransition,TouchActor,WindowBuildState
from fp_i05_reference.errors import FPI05Error

def test_complete_pair_window_creates_four_symbol_local_references():
 cfg,result,desc,agg,refs=golden_completed_n_window()
 assert len(refs.references)==4
 assert {(r.canonical_symbol,r.side) for r in refs.references}=={('ES',PriceSide.HIGH),('ES',PriceSide.LOW),('NQ',PriceSide.HIGH),('NQ',PriceSide.LOW)}

def test_reference_id_changes_with_price_revision():
 cfg,result,desc,agg,refs=golden_completed_n_window();changed=replace(agg,left=replace(agg.left,high=agg.left.high+1,semantic_hash='f'*64))
 changed=replace(changed,semantic_hash='e'*64)
 out=derive_reference_set(changed,desc.end_utc_ms)
 a=next(r for r in refs.references if r.canonical_symbol=='ES' and r.side is PriceSide.HIGH)
 b=next(r for r in out.references if r.canonical_symbol=='ES' and r.side is PriceSide.HIGH)
 assert a.reference_id!=b.reference_id

def test_hunter_touch_does_not_consume_reference():
 cfg,result,desc,agg,refs=golden_completed_n_window();r=refs.references[0]
 updated,event=transition_reference(r,ReferenceTransition.HUNTER_TOUCH_OBSERVED,desc.end_utc_ms+60000,'E',TouchActor.HUNTER)
 assert updated.state is ReferenceState.HUNTER_SEEN and updated.active_for_hunt

def test_protected_touch_consumes_reference():
 cfg,result,desc,agg,refs=golden_completed_n_window();r=refs.references[0]
 updated,event=transition_reference(r,ReferenceTransition.PROTECTED_TOUCH_CONSUMED,desc.end_utc_ms+60000,'E',TouchActor.PROTECTED)
 assert updated.state is ReferenceState.CONSUMED_BY_PROTECTED_TOUCH and not updated.active_for_hunt

def test_hunter_cannot_use_protected_transition():
 cfg,result,desc,agg,refs=golden_completed_n_window()
 with pytest.raises(FPI05Error):transition_reference(refs.references[0],ReferenceTransition.PROTECTED_TOUCH_CONSUMED,desc.end_utc_ms+60000,'E',TouchActor.HUNTER)

def test_consumed_reference_cannot_be_consumed_again():
 cfg,result,desc,agg,refs=golden_completed_n_window();u,_=transition_reference(refs.references[0],ReferenceTransition.PROTECTED_TOUCH_CONSUMED,desc.end_utc_ms+60000,'E',TouchActor.PROTECTED)
 with pytest.raises(FPI05Error):transition_reference(u,ReferenceTransition.PROTECTED_TOUCH_CONSUMED,desc.end_utc_ms+120000,'E2',TouchActor.PROTECTED)

def test_incomplete_window_cannot_create_references():
 cfg,result,desc,agg,refs=golden_completed_n_window();bad=replace(agg,left=replace(agg.left,state=WindowBuildState.INCOMPLETE))
 with pytest.raises(FPI05Error):derive_reference_set(bad,desc.end_utc_ms)

def test_expiry_is_terminal_for_hunt():
 cfg,result,desc,agg,refs=golden_completed_n_window();u,_=transition_reference(refs.references[0],ReferenceTransition.EXPIRED,desc.end_utc_ms+60000,'E')
 assert u.state is ReferenceState.EXPIRED and not u.active_for_hunt

def test_reference_event_time_must_be_monotonic_and_m1_aligned():
 cfg,result,desc,agg,refs=golden_completed_n_window();r=refs.references[0]
 with pytest.raises(FPI05Error): transition_reference(r,ReferenceTransition.HUNTER_TOUCH_OBSERVED,desc.end_utc_ms+1,'E',TouchActor.HUNTER)
