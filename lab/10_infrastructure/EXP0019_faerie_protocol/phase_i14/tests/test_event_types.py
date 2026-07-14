import pytest
from fp_i14_diagnostic import *
@pytest.mark.parametrize('event_type',list(TraceEventType))
def test_each_event_type_round_trips(event_type,manifests):
    m=manifests[ProductKind.INDICATOR];f=SemanticFact(1,1,event_type,'SEM-X',{'t':event_type.value},'READY');e=adapt_fact(m.product,m,f);assert e.event_type==event_type and len(e.semantic_hash)==64
