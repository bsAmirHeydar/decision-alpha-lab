from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Sequence
from .canonical import sha256
from .contracts import *
from .enums import *
from .maturity import determine_maturity
from .errors import ContractError

D0=Decimal("0"); D1=Decimal("1")

def path_hash(path:Sequence[PathObservation])->str:
    if not path: raise ContractError("empty_market_path","market path cannot be empty")
    last=-1
    for p in path:
        if p.sequence<=last: raise ContractError("non_monotonic_path_sequence","path sequence must be strictly increasing")
        last=p.sequence
    return sha256([p.to_dict() for p in path])

def _entry_executable(p:PathObservation,side:TradeSide)->Decimal: return p.ask if side==TradeSide.LONG else p.bid
def _exit_executable(p:PathObservation,side:TradeSide)->Decimal: return p.bid if side==TradeSide.LONG else p.ask

def _adverse_price(price:Decimal, side:TradeSide, is_entry:bool, slip:Decimal)->Decimal:
    if slip==0:return price
    if side==TradeSide.LONG:return price+slip if is_entry else price-slip
    return price-slip if is_entry else price+slip

def _fills_entry(t:TreatmentSibling,p:PathObservation)->bool:
    q=_entry_executable(p,t.side)
    if t.entry_style==EntryStyle.MARKET:return True
    assert t.entry_price is not None
    if t.side==TradeSide.LONG:
        return q<=t.entry_price if t.entry_style==EntryStyle.LIMIT else q>=t.entry_price
    return q>=t.entry_price if t.entry_style==EntryStyle.LIMIT else q<=t.entry_price

def evaluate_treatment(anchor:OpportunityAnchor,t:TreatmentSibling,path:Sequence[PathObservation],scenario:EconomicScenario,horizon_ms:int)->OutcomeCell:
    ph=path_hash(path); start=anchor.decision_time_ms; required_end=start+horizon_ms
    if not t.admissible:
        mat=determine_maturity(state=OutcomeState.REJECTED,terminal_reason=TerminalReason.REJECTED,observation_end_ms=path[-1].event_time_ms,required_end_ms=required_end,entry_time_ms=None,exit_time_ms=None)
        return OutcomeCell(anchor.opportunity_id,t.treatment_id,scenario.exact_key,horizon_ms,OutcomeState.REJECTED,TerminalReason.REJECTED,mat,None,None,None,None,D0,D0,D0,D0,D0,D0,D0,D0,None,None,ph,t.economic_envelope_hash,False,{"rejection_reason":t.rejection_reason})
    relevant=[p for p in path if p.event_time_ms>=start and p.event_time_ms<=required_end]
    if not relevant:
        mat=determine_maturity(state=OutcomeState.UNRESOLVED,terminal_reason=TerminalReason.DATA_GAP,observation_end_ms=path[-1].event_time_ms,required_end_ms=required_end,entry_time_ms=None,exit_time_ms=None)
        return OutcomeCell(anchor.opportunity_id,t.treatment_id,scenario.exact_key,horizon_ms,OutcomeState.UNRESOLVED,TerminalReason.DATA_GAP,mat,None,None,None,None,D0,D0,D0,D0,D0,D0,D0,D0,None,None,ph,t.economic_envelope_hash,False,{"reason":"no_observation_in_horizon"})
    entry=None; entry_time=None; filled=D0; open_qty=D0; best=D0; worst=D0; peak=D0; max_dd=D0; exit_price=None; exit_time=None; terminal=TerminalReason.NONE
    active_stop=t.stop_price
    best_exec=None
    for p in relevant:
        if p.gap:
            continue
        if entry is None:
            if p.event_time_ms>start+t.entry_expiry_ms and t.entry_style!=EntryStyle.MARKET: break
            if _fills_entry(t,p):
                q=min(D1,p.available_volume/t.volume) if t.volume>0 else D0
                if q<=0: continue
                filled=q; open_qty=q
                raw=t.entry_price if t.entry_style!=EntryStyle.MARKET and t.entry_price is not None else _entry_executable(p,t.side)
                entry=_adverse_price(raw,t.side,True,scenario.slippage_price)
                entry_time=p.event_time_ms; best_exec=_exit_executable(p,t.side)
                best=worst=D0; peak=D0
            continue
        ex=_exit_executable(p,t.side)
        move=(ex-entry) if t.side==TradeSide.LONG else (entry-ex)
        r=move*t.volume*t.cash_per_price_unit/t.maximum_loss_cash
        best=max(best,r); worst=min(worst,r); peak=max(peak,r); max_dd=max(max_dd,peak-r)
        if t.trail_distance is not None:
            if t.side==TradeSide.LONG:
                active_stop=max(active_stop,ex-t.trail_distance)
            else:
                active_stop=min(active_stop,ex+t.trail_distance)
        stop_hit=ex<=active_stop if t.side==TradeSide.LONG else ex>=active_stop
        target_hit=False if t.target_price is None else (ex>=t.target_price if t.side==TradeSide.LONG else ex<=t.target_price)
        if stop_hit:
            exit_price=_adverse_price(active_stop,t.side,False,scenario.slippage_price); exit_time=p.event_time_ms; terminal=TerminalReason.TRAIL if active_stop!=t.stop_price else TerminalReason.STOP; break
        if target_hit:
            exit_price=_adverse_price(t.target_price,t.side,False,scenario.slippage_price); exit_time=p.event_time_ms; terminal=TerminalReason.TARGET; break
    obs_end=relevant[-1].event_time_ms
    if entry is None:
        state=OutcomeState.UNFILLED if obs_end>=min(required_end,start+t.entry_expiry_ms) else OutcomeState.UNRESOLVED
        terminal=TerminalReason.ENTRY_EXPIRED if state==OutcomeState.UNFILLED else TerminalReason.END_OF_PATH
        mat=determine_maturity(state=state,terminal_reason=terminal,observation_end_ms=obs_end,required_end_ms=min(required_end,start+t.entry_expiry_ms),entry_time_ms=None,exit_time_ms=None)
        return OutcomeCell(anchor.opportunity_id,t.treatment_id,scenario.exact_key,horizon_ms,state,terminal,mat,None,None,None,None,D0,D0,D0,D0,D0,D0,D0,D0,None,None,ph,t.economic_envelope_hash,False,{})
    if exit_price is None:
        mark=_exit_executable(relevant[-1],t.side)
        exit_price=_adverse_price(mark,t.side,False,scenario.slippage_price); exit_time=obs_end
        state=OutcomeState.CENSORED if obs_end>=required_end else OutcomeState.OPEN
        terminal=TerminalReason.TIME if obs_end>=required_end else TerminalReason.END_OF_PATH
    else: state=OutcomeState.RESOLVED
    gross=((exit_price-entry) if t.side==TradeSide.LONG else (entry-exit_price))*t.volume*t.cash_per_price_unit*filled
    explicit=(t.estimated_cost_cash+scenario.commission_cash+scenario.financing_cash+scenario.gap_reserve_cash)*scenario.cost_multiplier*filled
    net=gross-explicit
    net_r=net/t.maximum_loss_cash
    mat=determine_maturity(state=state,terminal_reason=terminal,observation_end_ms=obs_end,required_end_ms=required_end,entry_time_ms=entry_time,exit_time_ms=exit_time)
    return OutcomeCell(anchor.opportunity_id,t.treatment_id,scenario.exact_key,horizon_ms,state,terminal,mat,entry_time,exit_time,entry,exit_price,filled,gross,explicit,net,net_r,best,worst,max_dd,entry_time-start if entry_time is not None else None,exit_time-entry_time if exit_time is not None and entry_time is not None else None,ph,t.economic_envelope_hash,net_r<=Decimal("-1"),{"active_stop":active_stop})
