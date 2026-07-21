from __future__ import annotations
from decimal import Decimal,InvalidOperation
from typing import Iterable
from .models import SafetyFinding,SafetyCode

def _d(value,default=None):
    try:return Decimal(str(value)) if value is not None else default
    except InvalidOperation:return default
class SafetyControlEngine:
    def evaluate(self,intent:dict,fixture:dict,seen_decisions:Iterable[str]=())->list[SafetyFinding]:
        out=[];rid=intent.get("request_id")
        if rid in set(seen_decisions):out.append(SafetyFinding(SafetyCode.DUPLICATE_DECISION,"request_id","Duplicate request identity"))
        if fixture.get("kill_switch_active"):out.append(SafetyFinding(SafetyCode.KILL_SWITCH_ACTIVE,"kill_switch","Kill switch is active"))
        if not fixture or fixture.get("bid") is None or fixture.get("ask") is None:out.append(SafetyFinding(SafetyCode.MISSING_QUOTE,"quote","Bid and ask are required"));return out
        if int(fixture.get("quote_age_ms",10**9))>int(fixture.get("max_quote_age_ms",0)):out.append(SafetyFinding(SafetyCode.STALE_QUOTE,"quote_age_ms","Quote is stale"))
        bid=_d(fixture.get("bid"));ask=_d(fixture.get("ask"));max_spread=_d(fixture.get("max_spread"),Decimal("0"))
        if bid is not None and ask is not None and ask-bid>max_spread:out.append(SafetyFinding(SafetyCode.EXCESSIVE_SPREAD,"spread","Spread exceeds allowed maximum",details={"spread":str(ask-bid),"max":str(max_spread)}))
        if not fixture.get("session_open",False):out.append(SafetyFinding(SafetyCode.CLOSED_SESSION,"session_open","Session is closed"))
        if not fixture.get("reconciliation_ok",False):out.append(SafetyFinding(SafetyCode.RECONCILIATION_MISMATCH,"reconciliation","Reconciliation mismatch"))
        entry=intent.get("entry") or {};kind=entry.get("kind")
        if kind not in {"MARKET","LIMIT","STOP","STOP_LIMIT"}:out.append(SafetyFinding(SafetyCode.UNSUPPORTED_ENTRY,"entry.kind","Entry kind is unsupported or unspecified"))
        tick=_d(fixture.get("tick_size"),Decimal("0"))
        for field,value in [("entry.price",entry.get("price")),("stop.price",(intent.get("stop") or {}).get("price"))]+[(f"targets[{i}].price",t.get("price")) for i,t in enumerate(intent.get("targets") or [])]:
            if value is not None and tick and _d(value)%tick!=0:out.append(SafetyFinding(SafetyCode.INVALID_TICK_ALIGNMENT,field,"Price is not aligned to tick size"))
        vol=_d((intent.get("volume_request") or {}).get("value"))
        if vol is not None:
            vmin=_d(fixture.get("volume_min"));vmax=_d(fixture.get("volume_max"));step=_d(fixture.get("volume_step"))
            if vol<vmin or vol>vmax or ((vol-vmin)%step)!=0:out.append(SafetyFinding(SafetyCode.INVALID_VOLUME,"volume_request.value","Volume violates min/max/step"))
        ep=_d(entry.get("price"));sp=_d((intent.get("stop") or {}).get("price"));min_stop=_d(fixture.get("stops_level"),Decimal("0"))
        if ep is not None and sp is not None and abs(ep-sp)<min_stop:out.append(SafetyFinding(SafetyCode.INVALID_STOP_DISTANCE,"stop.price","Stop distance is below platform minimum"))
        return out
