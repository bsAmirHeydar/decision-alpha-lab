from __future__ import annotations
from decimal import Decimal
from .contracts import BarObservation,PathEvent,PathSnapshot,CompiledTreatment
from .enums import *
from .errors import PathTransitionError
from .utils import dec
class IntrabarResolver:
    def resolve(self,treatment:CompiledTreatment,snapshot:PathSnapshot,bar:BarObservation,next_sequence:int)->tuple[PathEvent,...]:
        p=treatment.intrabar_policy
        if bar.known_time_ms-bar.close_time_ms>p.max_quote_age_ms and p.stale_quote is StaleQuotePolicy.REJECT:
            raise PathTransitionError('stale_observation','bar observation exceeded stale threshold')
        if snapshot.open_fraction<=0: return ()
        stop=snapshot.last_trail_price or snapshot.active_stop_price
        targets=[x.target_price for x in treatment.target.legs if x.target_price is not None]
        stop_hit=stop is not None and (bar.low<=stop if treatment.side.value=='long' else bar.high>=stop)
        target_hits=[x for x in targets if (bar.high>=x if treatment.side.value=='long' else bar.low<=x)]
        if not stop_hit and not target_hits:return ()
        seq=next_sequence; events=[]
        def ev(t,price,qty,reason):
            nonlocal seq; x=PathEvent(seq,t,bar.close_time_ms,bar.known_time_ms,dec(price),dec(qty),'intrabar_resolver',reason,{'policy_definition_id':p.definition_id,'side':treatment.side.value});seq+=1;events.append(x)
        if stop_hit and target_hits:
            policy=p.ambiguity
            if policy is AmbiguityPolicy.REJECT: raise PathTransitionError('ambiguous_bar','stop and target touched in the same bar')
            first='stop'
            if policy in (AmbiguityPolicy.TARGET_FIRST,AmbiguityPolicy.BEST_CASE): first='target'
            elif policy is AmbiguityPolicy.NEAREST_FIRST:
                anchor=snapshot.average_entry_price or bar.open; td=min(abs(x-anchor) for x in target_hits); sd=abs(stop-anchor); first='target' if td<sd else 'stop'
            elif policy is AmbiguityPolicy.WORST_CASE: first='stop'
            if first=='stop': ev(PathEventType.STOP_HIT,self._gap_price(treatment,bar,stop,True),snapshot.open_fraction,'intrabar_stop_first')
            else:
                target=self._nearest_target(snapshot.average_entry_price or bar.open,target_hits); ev(PathEventType.TARGET_HIT,self._gap_price(treatment,bar,target,False),snapshot.open_fraction,'intrabar_target_first')
        elif stop_hit: ev(PathEventType.STOP_HIT,self._gap_price(treatment,bar,stop,True),snapshot.open_fraction,'stop_hit')
        else:
            target=self._nearest_target(snapshot.average_entry_price or bar.open,target_hits); ev(PathEventType.TARGET_HIT,self._gap_price(treatment,bar,target,False),snapshot.open_fraction,'target_hit')
        return tuple(events)
    @staticmethod
    def _nearest_target(anchor,targets): return min(targets,key=lambda x:abs(x-anchor))
    @staticmethod
    def _gap_price(treatment,bar,level,is_stop):
        p=treatment.intrabar_policy; side=treatment.side.value
        gap_through=(bar.open<level if side=='long' and is_stop else bar.open>level if side=='short' and is_stop else bar.open>level if side=='long' else bar.open<level)
        if not gap_through:return level
        if p.gap is GapPolicy.REJECT: raise PathTransitionError('gap_through','gap crossed executable level')
        if p.gap is GapPolicy.FILL_AT_LEVEL:return level
        if p.gap is GapPolicy.FILL_AT_OPEN:return bar.open
        # worst executable
        if is_stop:return min(bar.open,level) if side=='long' else max(bar.open,level)
        return min(bar.open,level) if side=='short' else max(bar.open,level)
