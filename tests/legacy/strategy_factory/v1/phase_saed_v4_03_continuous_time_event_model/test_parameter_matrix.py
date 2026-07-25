import pytest
from dataclasses import replace
from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.enums import LatePolicy,ProjectionReducer,EventKind
from saed_v4_event_model.models import ProjectionFieldDefinition,EventProjectionDefinition
from helpers import batch

@pytest.mark.parametrize('lateness',[0,1,10,100,1000,5000,60000])
@pytest.mark.parametrize('priority',[-10,0,1,10,100])
def test_manifest_parameter_matrix(stream_nq,lateness,priority):
    s=ContinuousTimeEventService();m=replace(stream_nq,maximum_lateness_ms=lateness,source_priority=priority);assert s.register_stream(m).maximum_lateness_ms==lateness

@pytest.mark.parametrize('reducer',[ProjectionReducer.LAST,ProjectionReducer.COUNT,ProjectionReducer.SUM,ProjectionReducer.MIN,ProjectionReducer.MAX,ProjectionReducer.MEAN,ProjectionReducer.DELTA])
@pytest.mark.parametrize('window',[1,10,60,300])
def test_numeric_reducer_matrix(stream_nq,nq_events,reducer,window):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);f=ProjectionFieldDefinition('x',(EventKind.TRADE,),'price',reducer,window,('NQ',),False,None,0);d=EventProjectionDefinition('p','1',stream_nq.twin_id,(f,),'x');s.register_projection(d);s.append(batch(stream_nq,nq_events));p=s.project('p','1','2026-01-02T14:31:00Z','2026-01-02T14:30:03Z');assert p.values[0].value is not None

@pytest.mark.parametrize('known_offset',[0,1,2,5,10,30,60,120,300,600])
def test_future_suffix_matrix(stream_nq,nq_events,projection_def,known_offset):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.register_projection(projection_def);s.append(batch(stream_nq,nq_events));p=s.project(projection_def.projection_name,projection_def.exact_version,'2026-01-02T14:31:00Z','2026-01-02T14:30:03Z');assert p.twin_id==stream_nq.twin_id
