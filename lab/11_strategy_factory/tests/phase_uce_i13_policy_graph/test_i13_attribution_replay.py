from strategy_factory_policy_v3.contracts import AttributionOpportunity
from strategy_factory_policy_v3.attribution import incremental_value
from strategy_factory_policy_v3.replay import replay_many
from strategy_factory_policy_v3.golden import *
from strategy_factory_policy_v3.graph import compile_graph

def test_attribution_reconciles_total():
    ops=[AttributionOpportunity('a',True,False,1,0),AttributionOpportunity('b',True,True,1,2,True),AttributionOpportunity('c',True,True,1,1.5,False,True,.1)]
    r=incremental_value(ops); assert abs(sum(r.components.values())-r.incremental_total)<1e-9
def test_attribution_is_paired():
    r=incremental_value([AttributionOpportunity('a',True,True,0,1)]); assert r.paired_win_rate==1
def test_replay_sorts_by_known_time_and_is_stable():
    a=golden_admission();m=golden_manual();f=golden_fallback();au=golden_authority();g=compile_graph(golden_hybrid_graph(a,m,f,au),a);o1=golden_occurrence();o2=ContextOccurrence('occ:2',o1.context_type,6000,6000,o1.features,o1.views_present,o1.available_treatments,o1.available_risk_tiers,o1.candidate_actions);out1=golden_output();out2=ModelOutput(out1.model_id,out1.model_version,'occ:2',6000,7000,out1.action_probabilities,out1.utility,out1.rank_score,out1.treatment_distribution,out1.risk_distribution,out1.survival_probability,out1.tail_loss_probability,out1.uncertainty,out1.novelty,out1.calibration_state,out1.required_views,out1.feature_hash)
    d1,h1=replay_many(g,[o2,o1],m,f,au,admission=a,outputs={'occ:1':out1,'occ:2':out2});d2,h2=replay_many(g,[o1,o2],m,f,au,admission=a,outputs={'occ:1':out1,'occ:2':out2});assert h1==h2 and [x.occurrence_id for x in d1]==['occ:1','occ:2']
def test_trace_chain_verifies():
    from strategy_factory_policy_v3.engine import execute_policy
    from strategy_factory_policy_v3.evidence import TraceEntry,verify_trace
    a=golden_admission();m=golden_manual();f=golden_fallback();au=golden_authority();g=compile_graph(golden_hybrid_graph(a,m,f,au),a);d=execute_policy(g,golden_occurrence(),m,f,au,admission=a,model_output=golden_output())
    entries=[TraceEntry(**x) for x in d.trace]; assert verify_trace(entries)
def test_trace_tamper_fails():
    from dataclasses import replace
    from strategy_factory_policy_v3.engine import execute_policy
    from strategy_factory_policy_v3.evidence import TraceEntry,verify_trace
    a=golden_admission();m=golden_manual();f=golden_fallback();au=golden_authority();g=compile_graph(golden_hybrid_graph(a,m,f,au),a);d=execute_policy(g,golden_occurrence(),m,f,au,admission=a,model_output=golden_output())
    entries=[TraceEntry(**x) for x in d.trace]; entries[1]=replace(entries[1],status='tampered'); assert not verify_trace(entries)
