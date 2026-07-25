from .errors import FPI07Error
class ConfirmationStore:
    def __init__(self): self._pending={};self._results={};self._signals={};self._events={}
    def admit(self,pending,event):
        cid=pending.candidate.candidate_id
        if cid in self._results:return False
        existing=self._pending.get(cid)
        if existing and existing.pending_hash!=pending.pending_hash: raise FPI07Error("FP_CRC_PENDING_IDENTITY_COLLISION","candidate pending collision")
        self._pending[cid]=pending;self._events[event.event_id]=event;return existing is None
    def finalize(self,result,event):
        existing=self._results.get(result.candidate_id)
        if existing:
            if existing.result_hash!=result.result_hash: raise FPI07Error("FP_CRC_RESULT_IDENTITY_COLLISION","candidate finalized differently")
            return False
        self._results[result.candidate_id]=result;self._pending.pop(result.candidate_id,None);self._events[event.event_id]=event
        if result.confirmed_signal:self._signals[result.confirmed_signal.signal_id]=result.confirmed_signal
        return True
    @property
    def pending(self):return tuple(sorted(self._pending.values(),key=lambda x:x.pending_id))
    @property
    def results(self):return tuple(sorted(self._results.values(),key=lambda x:x.result_id))
    @property
    def signals(self):return tuple(sorted(self._signals.values(),key=lambda x:x.signal_id))
    @property
    def events(self):return tuple(sorted(self._events.values(),key=lambda x:(x.candidate_id,x.sequence,x.event_id)))
