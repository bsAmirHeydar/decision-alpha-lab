from __future__ import annotations
from .models import *
from .predicates import evaluate
from .path import PathLedger
from .costs import compute_cost
from .errors import PathError

def _zero_cost(model):return CostBreakdown(0,0,0,0,0,0,0,0,model.model_hash)
def _terminal_nontrade(spec,status,reason,decision_time,model,trigger=None):
    return OutcomeRow(spec.node_id,spec.node_hash,spec.action_class,status,reason,False,False,trigger,None,None,decision_time,None,spec.stop_price,spec.target_price,0,0,0,0,0,0,0,0,0,1.0,_zero_cost(model),tuple(),tuple(),spec.spec_hash,('No order was simulated for this structural action.',))

def simulate(spec:ExecutionSpec,context:ContextSnapshot,observations:list[PriceObservation],policy:OutcomePolicy,cost_model:CostModel)->OutcomeRow:
    if spec.action_class=='skip':return _terminal_nontrade(spec,'skipped','skip_action',context.decision_time_ms,cost_model)
    if spec.action_class=='abstain':return _terminal_nontrade(spec,'abstained','abstain_action',context.decision_time_ms,cost_model)
    fmap=context.feature_map();trigger=True
    if spec.trigger_ref:
        trigger=evaluate(spec.trigger_operator,fmap.get(spec.trigger_ref),spec.trigger_expected)
        if not trigger:return _terminal_nontrade(spec,'trigger_rejected','trigger_false',context.decision_time_ms,cost_model,False)
    obs=[o for o in observations if o.symbol==context.symbol]
    if policy.fail_on_symbol_mismatch and len(obs)!=len(observations):raise PathError('symbol mismatch in observation path')
    if len(obs)>policy.maximum_observations:raise PathError('observation budget exceeded')
    if policy.strict_monotonic_sequences and any(b.sequence<=a.sequence for a,b in zip(obs,obs[1:])):raise PathError('non-monotonic observation sequence')
    if any(o.observed_at_ms<context.decision_time_ms for o in obs):raise PathError('pre-decision observation in outcome path')
    entry_time=None;entry_price=None;entry_spread=0.0;remaining=1.0;realized=0.0;trail_stop=spec.stop_price;partial_used=False;trail_used=False;ambiguous=False;ledger=None;used=[]
    for o in obs:
        used.append(o.observation_hash)
        if entry_time is None:
            if o.observed_at_ms>spec.entry_expiration_ms:break
            touched=o.high>=spec.entry_price if spec.direction==1 else o.low<=spec.entry_price
            if not touched:continue
            gap=(o.open-spec.entry_price)*spec.direction>0
            if gap and policy.gap_policy=='exclude':continue
            entry_price=o.open if gap and policy.gap_policy=='conservative_open' else spec.entry_price
            entry_time=o.observed_at_ms;entry_spread=o.spread_points;risk=(entry_price-spec.stop_price)*spec.direction
            if risk<=0:raise PathError('non-positive risk after gap fill')
            ledger=PathLedger(spec.direction,entry_price,risk,policy.maximum_path_events_per_row);ledger.append('registered',context.decision_time_ms,spec.entry_price);ledger.append('trigger_accepted',context.decision_time_ms,spec.entry_price);ledger.append('filled',entry_time,entry_price)
        risk=(entry_price-spec.stop_price)*spec.direction;ledger.update_extremes(o,remaining)
        if spec.partial_fraction>0 and not partial_used and ledger.mfe>=spec.partial_activation_r*risk:
            px=entry_price+spec.direction*spec.partial_activation_r*risk;realized+=spec.partial_fraction*((px-entry_price)*spec.direction);remaining-=spec.partial_fraction;partial_used=True;ledger.append('partial_exit',o.observed_at_ms,px,remaining)
        if spec.trail_activation_r>0 and not trail_used and ledger.mfe>=spec.trail_activation_r*risk:
            trail_stop=max(trail_stop,entry_price) if spec.direction==1 else min(trail_stop,entry_price);trail_used=True;ledger.append('trail_activated',o.observed_at_ms,trail_stop,remaining);ledger.append('stop_moved',o.observed_at_ms,trail_stop,remaining)
        stop_hit=o.low<=trail_stop if spec.direction==1 else o.high>=trail_stop
        target_hit=spec.target_price is not None and (o.high>=spec.target_price if spec.direction==1 else o.low<=spec.target_price)
        if stop_hit and target_hit:
            ambiguous=True
            if policy.ambiguity_policy in ('exclude','require_higher_fidelity'):
                cost=compute_cost(cost_model,risk,entry_spread,o.spread_points);gross=realized/risk
                return OutcomeRow(spec.node_id,spec.node_hash,spec.action_class,'ambiguous','ambiguous_bar',True,True,True,entry_time,entry_price,o.observed_at_ms,o.close,trail_stop,spec.target_price,realized,gross,gross-cost.total_cost_r,ledger.mfe,ledger.mae,ledger.mfe/risk,ledger.mae/risk,o.observed_at_ms-entry_time,entry_time-context.decision_time_ms,remaining,cost,tuple(ledger.events),tuple(used),spec.spec_hash,('Intrabar ordering was not identifiable at available fidelity.',))
        choose_stop=stop_hit and (not target_hit or policy.ambiguity_policy=='stop_first')
        choose_target=target_hit and (not stop_hit or policy.ambiguity_policy=='target_first')
        if choose_stop:
            px=trail_stop;gross_points=realized+remaining*((px-entry_price)*spec.direction);cost=compute_cost(cost_model,risk,entry_spread,o.spread_points);ledger.append('closed',o.observed_at_ms,px,0)
            reason='partial_then_stop' if partial_used else 'stop';gross=gross_points/risk
            return OutcomeRow(spec.node_id,spec.node_hash,spec.action_class,'closed',reason,True,ambiguous,True,entry_time,entry_price,o.observed_at_ms,px,trail_stop,spec.target_price,gross_points,gross,gross-cost.total_cost_r,ledger.mfe,ledger.mae,ledger.mfe/risk,ledger.mae/risk,o.observed_at_ms-entry_time,entry_time-context.decision_time_ms,0,cost,tuple(ledger.events),tuple(used),spec.spec_hash,('Reference deterministic counterfactual simulation only.',))
        if choose_target:
            px=spec.target_price;gross_points=realized+remaining*((px-entry_price)*spec.direction);cost=compute_cost(cost_model,risk,entry_spread,o.spread_points);ledger.append('closed',o.observed_at_ms,px,0);gross=gross_points/risk
            return OutcomeRow(spec.node_id,spec.node_hash,spec.action_class,'closed','target',True,ambiguous,True,entry_time,entry_price,o.observed_at_ms,px,trail_stop,spec.target_price,gross_points,gross,gross-cost.total_cost_r,ledger.mfe,ledger.mae,ledger.mfe/risk,ledger.mae/risk,o.observed_at_ms-entry_time,entry_time-context.decision_time_ms,0,cost,tuple(ledger.events),tuple(used),spec.spec_hash,('Reference deterministic counterfactual simulation only.',))
        if spec.maximum_holding_ms>0 and o.observed_at_ms-entry_time>=spec.maximum_holding_ms:
            px=o.bid if spec.direction==1 and o.bid is not None else o.ask if spec.direction==-1 and o.ask is not None else o.close;gross_points=realized+remaining*((px-entry_price)*spec.direction);cost=compute_cost(cost_model,risk,entry_spread,o.spread_points);ledger.append('closed',o.observed_at_ms,px,0);gross=gross_points/risk
            return OutcomeRow(spec.node_id,spec.node_hash,spec.action_class,'closed','partial_then_time' if partial_used else 'time',True,ambiguous,True,entry_time,entry_price,o.observed_at_ms,px,trail_stop,spec.target_price,gross_points,gross,gross-cost.total_cost_r,ledger.mfe,ledger.mae,ledger.mfe/risk,ledger.mae/risk,o.observed_at_ms-entry_time,entry_time-context.decision_time_ms,0,cost,tuple(ledger.events),tuple(used),spec.spec_hash,('Reference deterministic counterfactual simulation only.',))
    if entry_time is None:return _terminal_nontrade(spec,'entry_expired','entry_expired',spec.entry_expiration_ms,cost_model,True)
    o=obs[-1];risk=(entry_price-spec.stop_price)*spec.direction;px=o.close;gross_points=realized+remaining*((px-entry_price)*spec.direction);cost=compute_cost(cost_model,risk,entry_spread,o.spread_points);ledger.append('closed',o.observed_at_ms,px,0);gross=gross_points/risk
    return OutcomeRow(spec.node_id,spec.node_hash,spec.action_class,'closed','time',True,ambiguous,True,entry_time,entry_price,o.observed_at_ms,px,trail_stop,spec.target_price,gross_points,gross,gross-cost.total_cost_r,ledger.mfe,ledger.mae,ledger.mfe/risk,ledger.mae/risk,o.observed_at_ms-entry_time,entry_time-context.decision_time_ms,0,cost,tuple(ledger.events),tuple(used),spec.spec_hash,('Observation path ended before the configured maximum holding time.',))
