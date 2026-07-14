import pytest
from fp_i13_release import *
from fp_i13_release.errors import FPI13Error
from fp_i13_release.replay import ReplayReducer
def test_identical_duplicate_ignored(fixture,instance):
 r=ReplayReducer(fixture,instance);e=fixture.events[0];assert r.apply(e)==ReplayDisposition.APPLIED;assert r.apply(e)==ReplayDisposition.DUPLICATE_IGNORED;assert r.duplicates==1
def test_event_collision_fails(fixture,instance):
 r=ReplayReducer(fixture,instance);e=fixture.events[0];r.apply(e);bad=ReplayEvent(e.sequence+1,e.event_time+1,e.event_type,e.semantic_id,'1'*64,e.source_revision_id,event_id=e.computed_event_id)
 with pytest.raises(FPI13Error):r.apply(bad)
def test_sequence_regression_fails(fixture,instance):
 r=ReplayReducer(fixture,instance);r.apply(fixture.events[1])
 with pytest.raises(FPI13Error):r.apply(fixture.events[0])
