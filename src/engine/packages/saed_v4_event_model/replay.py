from .projections import build_projection
from .models import EventReplayReceipt
from .errors import ReplayError

def replay_projection(definition,events,known_as_of,event_as_of,expected_state_hash,watermarks=(),late_event_ids=(),gaps=()):
    observed=build_projection(definition,events,known_as_of,event_as_of,watermarks,late_event_ids,gaps)
    status='pass' if observed.state_hash==expected_state_hash else 'fail'
    receipt=EventReplayReceipt(definition.projection_id,known_as_of,event_as_of,expected_state_hash,observed.state_hash,len(events),status)
    if status!='pass':raise ReplayError('projection replay mismatch')
    return receipt
