from __future__ import annotations
from dataclasses import asdict
from .contracts import RiskReservation,PortfolioLimits,OpportunityCandidate
from .enums import ReservationStatus
from .canonical import canonical_sha256
from .errors import PortfolioError
class ReservationLedger:
    def __init__(self,limits:PortfolioLimits,as_of_ms:int=0): self.limits=limits;self.as_of_ms=as_of_ms;self.entries=[];self._active={}
    @property
    def head_hash(self): return self.entries[-1].entry_hash if self.entries else '0'*64
    @property
    def ledger_hash(self): return canonical_sha256([asdict(x) for x in self.entries])
    def _sum(self,field,value): return sum(r.risk_units for r in self._active.values() if getattr(r,field)==value and r.status is ReservationStatus.RESERVED)
    def total(self): return sum(r.risk_units for r in self._active.values() if r.status is ReservationStatus.RESERVED)
    def reserve(self,c:OpportunityCandidate,risk:float,expires_at_ms:int):
        if risk<=0: raise PortfolioError('invalid_reservation_risk','risk must be positive')
        checks=[(self.total()+risk<=self.limits.total_risk,'total'),(self._sum('symbol',c.symbol)+risk<=self.limits.per_symbol_risk,'symbol'),(self._sum('currency',c.currency)+risk<=self.limits.per_currency_risk,'currency'),(self._sum('context_id',c.context_id)+risk<=self.limits.per_context_risk,'context'),(self._sum('cluster_id',c.cluster_id)+risk<=self.limits.per_cluster_risk,'cluster')]
        failed=[n for ok,n in checks if not ok]
        if failed: raise PortfolioError('reservation_limit_breach','risk cannot be reserved',{'limits':failed})
        seq=len(self.entries)+1;rid=f'reservation:{c.candidate_id}:{seq}';prev=self.head_hash
        payload={'reservation_id':rid,'candidate_id':c.candidate_id,'context_id':c.context_id,'symbol':c.symbol,'currency':c.currency,'cluster_id':c.cluster_id,'risk_units':risk,'created_at_ms':self.as_of_ms,'expires_at_ms':expires_at_ms,'status':ReservationStatus.RESERVED,'ledger_sequence':seq,'previous_hash':prev}
        entry=RiskReservation(**payload,entry_hash=canonical_sha256(payload));self.entries.append(entry);self._active[rid]=entry;return entry
    def release(self,reservation_id,status=ReservationStatus.RELEASED):
        old=self._active.get(reservation_id)
        if not old: raise PortfolioError('unknown_reservation','reservation not found')
        seq=len(self.entries)+1;prev=self.head_hash
        payload={k:v for k,v in asdict(old).items() if k!='entry_hash'};payload.update(status=status,ledger_sequence=seq,previous_hash=prev)
        entry=RiskReservation(**payload,entry_hash=canonical_sha256(payload));self.entries.append(entry);self._active[reservation_id]=entry;return entry
    def expire(self,now_ms):
        out=[]
        for rid,r in list(self._active.items()):
            if r.status is ReservationStatus.RESERVED and r.expires_at_ms<=now_ms: out.append(self.release(rid))
        return tuple(out)
