from dataclasses import replace
from .contracts import *
from .canonical import *
from .quota import PaperQuotaStore
from .ledger import ReconciliationLedger
from .order import make_order,transition_order
from .position import position_from_fills

def _fill(order,price,volume,now,seq):
    payload={"order":order.order_id,"price":price,"volume":volume,"time":now,"seq":seq}
    fid=stable_id("FPFILL",payload)
    return PaperFill(fid,order.order_id,volume,price,now,seq,sha256(payload))

def simulate(plan:ExecutionPlan,policy:PaperPolicyConfig,scenario:PaperScenario,quote:QuoteSnapshot,now:int,fill_slippage_price:float=0.0)->PaperRunResult:
    ledger=ReconciliationLedger(); quota_store=PaperQuotaStore(); fills=[]; position=None; order=None; reasons=[]
    if plan.state!=PlanState.READY:
        q=quota_store.get(plan.quota_key_id); ledger.append(LedgerEventType.PLAN_BLOCKED,plan.plan_id,now,{"plan":plan.plan_hash},plan.reason_codes)
        return _result(scenario,plan,q,order,fills,position,ledger,HealthState.BLOCKED,plan.reason_codes)
    ledger.append(LedgerEventType.PLAN_CREATED,plan.plan_id,now,{"plan":plan.plan_hash})
    q=quota_store.reserve(plan,policy); ledger.append(LedgerEventType.QUOTA_RESERVED,q.paper_reservation_id,now,{"record":q.record_hash})
    if q.state==QuotaState.CONSUMED: ledger.append(LedgerEventType.QUOTA_CONSUMED,q.paper_reservation_id,now,{"event":q.consumed_event.value})
    if scenario==PaperScenario.QUOTE_UNAVAILABLE:
        q=quota_store.release(plan.quota_key_id,policy,"FP_PAPER_QUOTE_UNAVAILABLE")
        if q.state==QuotaState.RELEASED: ledger.append(LedgerEventType.QUOTA_RELEASED,q.paper_reservation_id,now,{"reason":"FP_PAPER_QUOTE_UNAVAILABLE"})
        return _result(scenario,plan,q,None,(),None,ledger,HealthState.DEGRADED,("FP_PAPER_QUOTE_UNAVAILABLE",))
    if scenario==PaperScenario.GEOMETRY_DRIFT:
        q=quota_store.release(plan.quota_key_id,policy,"FP_PAPER_GEOMETRY_REVALIDATION_FAILED")
        if q.state==QuotaState.RELEASED: ledger.append(LedgerEventType.QUOTA_RELEASED,q.paper_reservation_id,now,{"reason":"FP_PAPER_GEOMETRY_REVALIDATION_FAILED"})
        return _result(scenario,plan,q,None,(),None,ledger,HealthState.DEGRADED,("FP_PAPER_GEOMETRY_REVALIDATION_FAILED",))
    order=make_order(plan,now); ledger.append(LedgerEventType.ORDER_CREATED,order.order_id,now,{"order":order.order_hash})
    order=transition_order(order,OrderState.VALIDATED,now+1); ledger.append(LedgerEventType.ORDER_VALIDATED,order.order_id,now+1,{"order":order.order_hash})
    order=transition_order(order,OrderState.ATTEMPTED,now+2); ledger.append(LedgerEventType.ORDER_ATTEMPTED,order.order_id,now+2,{"order":order.order_hash})
    q=quota_store.trigger(plan.quota_key_id,PaperConsumeEvent.ORDER_ATTEMPTED,policy,"FP_PAPER_ORDER_ATTEMPTED")
    if q.state==QuotaState.CONSUMED and not any(e.event_type==LedgerEventType.QUOTA_CONSUMED for e in ledger.events): ledger.append(LedgerEventType.QUOTA_CONSUMED,q.paper_reservation_id,now+2,{"event":q.consumed_event.value})
    if scenario==PaperScenario.REJECT_AT_ATTEMPT:
        order=transition_order(order,OrderState.REJECTED,now+3,("FP_PAPER_ORDER_REJECTED",)); ledger.append(LedgerEventType.ORDER_REJECTED,order.order_id,now+3,{"order":order.order_hash})
        q=quota_store.release(plan.quota_key_id,policy,"FP_PAPER_ORDER_REJECTED")
        if q.state==QuotaState.RELEASED: ledger.append(LedgerEventType.QUOTA_RELEASED,q.paper_reservation_id,now+3,{"reason":"FP_PAPER_ORDER_REJECTED"})
        return _result(scenario,plan,q,order,(),None,ledger,HealthState.DEGRADED,order.reason_codes)
    order=transition_order(order,OrderState.ACCEPTED,now+3); ledger.append(LedgerEventType.ORDER_ACCEPTED,order.order_id,now+3,{"order":order.order_hash})
    q=quota_store.trigger(plan.quota_key_id,PaperConsumeEvent.ORDER_ACCEPTED,policy,"FP_PAPER_ORDER_ACCEPTED")
    if q.state==QuotaState.CONSUMED and not any(e.event_type==LedgerEventType.QUOTA_CONSUMED for e in ledger.events): ledger.append(LedgerEventType.QUOTA_CONSUMED,q.paper_reservation_id,now+3,{"event":q.consumed_event.value})
    if scenario==PaperScenario.ACCEPT_THEN_CANCEL:
        order=transition_order(order,OrderState.CANCELLED,now+4,("FP_PAPER_ORDER_CANCELLED",)); ledger.append(LedgerEventType.ORDER_CANCELLED,order.order_id,now+4,{"order":order.order_hash})
        q=quota_store.release(plan.quota_key_id,policy,"FP_PAPER_ORDER_CANCELLED")
        if q.state==QuotaState.RELEASED: ledger.append(LedgerEventType.QUOTA_RELEASED,q.paper_reservation_id,now+4,{"reason":"FP_PAPER_ORDER_CANCELLED"})
        return _result(scenario,plan,q,order,(),None,ledger,HealthState.DEGRADED,order.reason_codes)
    entry=plan.geometry.planned_entry + (fill_slippage_price if plan.direction==TradeDirection.BUY else -fill_slippage_price)
    if abs(fill_slippage_price)>abs(plan.geometry.worst_case_entry-plan.geometry.planned_entry)+1e-12: raise ValueError("fill slippage exceeds configured budget")
    if scenario==PaperScenario.PARTIAL_THEN_FILL:
        v1=floor_step(plan.sizing.volume/2,0.01)
        if v1<=0: v1=plan.sizing.volume
        f1=_fill(order,entry,v1,now+4,1); fills.append(f1)
        order=transition_order(order,OrderState.PARTIALLY_FILLED,now+4,filled_volume=v1,average_fill_price=entry); ledger.append(LedgerEventType.ORDER_PARTIAL_FILL,order.order_id,now+4,{"fill":f1.fill_hash})
        q=quota_store.trigger(plan.quota_key_id,PaperConsumeEvent.FIRST_FILL,policy,"FP_PAPER_FIRST_FILL")
        if q.state==QuotaState.CONSUMED and not any(e.event_type==LedgerEventType.QUOTA_CONSUMED for e in ledger.events): ledger.append(LedgerEventType.QUOTA_CONSUMED,q.paper_reservation_id,now+4,{"event":q.consumed_event.value})
        rem=plan.sizing.volume-v1
        if rem>1e-12:
            f2=_fill(order,entry,rem,now+5,2); fills.append(f2)
            order=transition_order(order,OrderState.FILLED,now+5,filled_volume=plan.sizing.volume,average_fill_price=entry); ledger.append(LedgerEventType.ORDER_FILLED,order.order_id,now+5,{"fill":f2.fill_hash})
    else:
        f=_fill(order,entry,plan.sizing.volume,now+4,1); fills.append(f)
        order=transition_order(order,OrderState.FILLED,now+4,filled_volume=plan.sizing.volume,average_fill_price=entry); ledger.append(LedgerEventType.ORDER_FILLED,order.order_id,now+4,{"fill":f.fill_hash})
        q=quota_store.trigger(plan.quota_key_id,PaperConsumeEvent.FIRST_FILL,policy,"FP_PAPER_FIRST_FILL")
        if q.state==QuotaState.CONSUMED and not any(e.event_type==LedgerEventType.QUOTA_CONSUMED for e in ledger.events): ledger.append(LedgerEventType.QUOTA_CONSUMED,q.paper_reservation_id,now+4,{"event":q.consumed_event.value})
    position=position_from_fills(plan,order,tuple(fills),now+5); ledger.append(LedgerEventType.POSITION_OPENED,position.position_id,now+5,{"position":position.position_hash})
    ledger.append(LedgerEventType.RECONCILED,plan.plan_id,now+6,{"plan":plan.plan_hash,"quota":q.record_hash,"order":order.order_hash,"position":position.position_hash})
    return _result(scenario,plan,q,order,tuple(fills),position,ledger,HealthState.READY,())

def _result(scenario,plan,quota,order,fills,position,ledger,health,reasons):
    payload={"scenario":scenario,"plan":plan.plan_hash if plan else "","quota":quota.record_hash,"order":order.order_hash if order else "","fills":[f.fill_hash for f in fills],"position":position.position_hash if position else "","chain":ledger.chain_head,"health":health,"reasons":tuple(sorted(set(reasons)))}
    return PaperRunResult(stable_id("FPRUN",payload),scenario,plan,quota,order,tuple(fills),position,tuple(ledger.events),health,tuple(sorted(set(reasons))),sha256(payload))
