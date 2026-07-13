from __future__ import annotations
import threading
from typing import Mapping
from .contracts import RuntimeDecision
from .errors import DuplicateDecisionError
class DecisionJournal:
    def __init__(self):self._lock=threading.RLock();self._by_request={};self._by_occurrence={}
    def get(self,request_id:str)->RuntimeDecision|None:
        with self._lock:return self._by_request.get(request_id)
    def append(self,decision:RuntimeDecision)->RuntimeDecision:
        with self._lock:
            prior=self._by_request.get(decision.request_id)
            if prior is not None:
                if prior.decision_hash!=decision.decision_hash:raise DuplicateDecisionError('duplicate_request_conflict','request already has a different decision')
                return prior
            occ=self._by_occurrence.get(decision.occurrence_id)
            if occ is not None and occ.decision_hash!=decision.decision_hash:raise DuplicateDecisionError('duplicate_occurrence_conflict','occurrence already decided under another request')
            self._by_request[decision.request_id]=decision;self._by_occurrence[decision.occurrence_id]=decision;return decision
    def snapshot(self)->tuple[RuntimeDecision,...]:
        with self._lock:return tuple(sorted(self._by_request.values(),key=lambda d:(d.known_time_ms,d.request_id)))
    def restore(self,decisions):
        for d in decisions:self.append(d)
