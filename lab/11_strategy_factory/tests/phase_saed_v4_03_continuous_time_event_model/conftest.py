import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
sys.path.insert(0,str(Path(__file__).parent))
from saed_v4_event_model.conformance import manifest,event,projection
from saed_v4_event_model.models import EventBatch
from saed_v4_event_model.canonical import content_hash
@pytest.fixture
def root():return ROOT
@pytest.fixture
def examples(root):return root/'lab/11_strategy_factory/examples/saed_v4_03'
@pytest.fixture
def stream_nq(examples):return manifest(json.loads((examples/'golden_stream_nq.json').read_text()))
@pytest.fixture
def stream_es(examples):return manifest(json.loads((examples/'golden_stream_es.json').read_text()))
@pytest.fixture
def nq_events(examples):return tuple(event(x) for x in json.loads((examples/'golden_events_nq.json').read_text()))
@pytest.fixture
def es_events(examples):return tuple(event(x) for x in json.loads((examples/'golden_events_es.json').read_text()))
@pytest.fixture
def projection_def(examples):return projection(json.loads((examples/'golden_projection_definition.json').read_text()))
def batch(stream,events,bid='batch'):
    return EventBatch(bid,stream.stream_id,stream.exact_version,tuple(events),content_hash([x.envelope_hash for x in events]))
