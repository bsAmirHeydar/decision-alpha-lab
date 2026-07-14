from __future__ import annotations
from .lifecycle import LifecycleMachine
class TransitionLedger:
    def __init__(self,machine:LifecycleMachine):self.machine=machine;self.events=[];self.ids=set()
    def request(self,*args,**kwargs):
        kwargs['sequence']=len(self.events)+1
        e=self.machine.request(*args,**kwargs)
        if e.event_id not in self.ids:self.events.append(e);self.ids.add(e.event_id)
        return e
