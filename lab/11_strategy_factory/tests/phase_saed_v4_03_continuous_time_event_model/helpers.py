from saed_v4_event_model.models import EventBatch
from saed_v4_event_model.canonical import content_hash

def batch(stream,events,bid='batch'):
    return EventBatch(bid,stream.stream_id,stream.exact_version,tuple(events),content_hash([x.envelope_hash for x in events]))
