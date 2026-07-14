from __future__ import annotations
from .registry import EventStreamRegistry,ProjectionRegistry
from .watermarks import WatermarkTracker
from .journal import EventJournal
from .projections import build_projection
from .gaps import detect_time_gaps
from .alignment import align_latest
class ContinuousTimeEventService:
    def __init__(self):
        self.streams=EventStreamRegistry();self.projections=ProjectionRegistry();self.watermarks=WatermarkTracker();self.journal=EventJournal(self.streams,self.watermarks);self._projection_sequence=0
    def register_stream(self,manifest):return self.streams.register(manifest)
    def register_projection(self,definition):return self.projections.register(definition)
    def append(self,batch):return self.journal.append(batch)
    def project(self,name,version,known_as_of,event_as_of,maximum_gap_ms=None):
        d=self.projections.get(name,version);events=self.journal.effective(d.twin_id,known_as_of,event_as_of);gaps=detect_time_gaps(events,maximum_gap_ms) if maximum_gap_ms else ();self._projection_sequence+=1
        return build_projection(d,events,known_as_of,event_as_of,self.watermarks.all_states(),tuple(x.event_id for x in self.watermarks.late_records()),gaps,self._projection_sequence)
    def align(self,twin_id,subjects,known_as_of,event_as_of,maximum_staleness_ms):return align_latest(twin_id,self.journal.effective(twin_id,known_as_of,event_as_of),subjects,known_as_of,event_as_of,maximum_staleness_ms)
