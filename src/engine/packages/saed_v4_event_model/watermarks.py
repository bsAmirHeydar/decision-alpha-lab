from __future__ import annotations
from dataclasses import replace
from .models import WatermarkState,LateEventRecord
from .enums import AppendDisposition,LatePolicy
from .canonical import normalize_time,parse_time
from .temporal import subtract_ms
class WatermarkTracker:
    def __init__(self):self._states={};self._late=[]
    def state(self,manifest):return self._states.get(manifest.stream_id,WatermarkState(manifest.stream_id,None,None,manifest.maximum_lateness_ms,0,0))
    def classify(self,manifest,event):
        st=self.state(manifest);late=bool(st.watermark_time and parse_time(event.event_time)<parse_time(st.watermark_time))
        if not late:return False,None
        disp={LatePolicy.ACCEPT_FLAG:AppendDisposition.COMMITTED,LatePolicy.QUARANTINE:AppendDisposition.QUARANTINED,LatePolicy.REJECT:AppendDisposition.REJECTED}[manifest.late_policy]
        rec=LateEventRecord(event.event_id,event.stream_id,event.event_time,st.watermark_time,manifest.late_policy,disp,'event_time precedes stream watermark');return True,rec
    def observe(self,manifest,event,late:bool):
        st=self.state(manifest);mx=event.event_time if st.maximum_event_time is None or parse_time(event.event_time)>parse_time(st.maximum_event_time) else st.maximum_event_time
        wm=subtract_ms(mx,manifest.maximum_lateness_ms)
        st=WatermarkState(manifest.stream_id,mx,wm,manifest.maximum_lateness_ms,st.accepted_events+1,st.late_events+(1 if late else 0));self._states[manifest.stream_id]=st;return st
    def add_late(self,rec):self._late.append(rec)
    def late_records(self):return tuple(self._late)
    def all_states(self):return tuple(self._states[k] for k in sorted(self._states))
