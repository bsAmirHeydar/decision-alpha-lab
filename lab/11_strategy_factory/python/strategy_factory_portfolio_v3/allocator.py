from __future__ import annotations
from collections import defaultdict
from .contracts import AllocationItem,AllocationPlan,OpportunityBatch,PortfolioLimits,DependenceModel,CapacityQuote
from .enums import OpportunityStatus,AllocationStatus,Side,ConflictPolicy
from .queue import rank_batch
from .dependence import marginal_risk
from .reservations import ReservationLedger
from .interactions import resolve_symbol_conflicts
from .canonical import canonical_sha256

def allocate(batch:OpportunityBatch,model:DependenceModel,limits:PortfolioLimits,quotes:dict[str,CapacityQuote],conflict_policy:ConflictPolicy=ConflictPolicy.DENY):
    ranked=rank_batch(batch);eligible=[x for x in ranked if x.status is OpportunityStatus.ELIGIBLE]
    blocked=set();by_symbol=defaultdict(list)
    for r in eligible:by_symbol[r.candidate.symbol].append(r.candidate)
    for group in by_symbol.values():
        d=resolve_symbol_conflicts(group,conflict_policy);blocked.update(d.blocked_candidate_ids)
    ledger=ReservationLedger(limits,batch.as_of_ms);selected=[];selected_candidates=[];rejected=[];gross=net=turnover=0.0
    for r in eligible:
        c=r.candidate;q=quotes.get(c.candidate_id)
        reasons=[]
        if c.candidate_id in blocked:rejected.append(c.candidate_id);continue
        if q is None or not q.market_open or q.max_risk_units<=0:rejected.append(c.candidate_id);continue
        if c.liquidity_score<limits.min_liquidity_score or c.turnover_cost>limits.max_turnover_cost:rejected.append(c.candidate_id);continue
        if len(selected)>=limits.max_positions:rejected.append(c.candidate_id);continue
        risk=min(c.requested_risk,q.max_risk_units,limits.total_risk-ledger.total())
        if risk<=0:rejected.append(c.candidate_id);continue
        mr=marginal_risk(c,selected_candidates,model)*(risk/max(c.requested_risk,1e-12))
        adjusted=max(0.0,r.score/(1+mr+q.impact_bps/10000))
        try:res=ledger.reserve(c,risk,min(c.expires_at_ms,batch.as_of_ms+86_400_000))
        except Exception: rejected.append(c.candidate_id);continue
        gross+=risk;net+=risk*(1 if c.side is Side.LONG else -1);turnover+=c.turnover_cost
        if gross>limits.max_gross_exposure or abs(net)>limits.max_net_exposure or turnover>limits.max_turnover_cost:
            ledger.release(res.reservation_id);gross-=risk;net-=risk*(1 if c.side is Side.LONG else -1);turnover-=c.turnover_cost;rejected.append(c.candidate_id);continue
        selected_candidates.append(c);selected.append(AllocationItem(c.candidate_id,c.context_id,c.symbol,c.side,risk,q.max_risk_units,mr,adjusted,res.reservation_id,tuple(reasons)))
    rejected+= [x.candidate.candidate_id for x in ranked if x.status is not OpportunityStatus.ELIGIBLE]
    contexts=len(set(x.context_id for x in selected));checks={'reserved_risk':abs(sum(x.allocated_risk for x in selected)-ledger.total())<1e-9,'total_risk':ledger.total()<=limits.total_risk,'gross':gross<=limits.max_gross_exposure,'net':abs(net)<=limits.max_net_exposure,'position_count':len(selected)<=limits.max_positions,'context_count':contexts>=limits.min_context_count}
    if not selected:status=AllocationStatus.ABSTAIN;reasons=('no_feasible_allocation',)
    elif all(checks.values()):status=AllocationStatus.ALLOCATED;reasons=()
    else:status=AllocationStatus.PARTIAL;reasons=tuple(k for k,v in checks.items() if not v)
    plan=AllocationPlan('allocation:'+batch.batch_id,'1.0.0',batch.batch_hash,model.model_hash,limits.limits_hash,batch.as_of_ms,status,tuple(selected),tuple(sorted(set(rejected))),ledger.total(),gross,net,turnover,contexts,checks,reasons)
    return plan,ledger
