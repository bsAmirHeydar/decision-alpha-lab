from dataclasses import replace
from strategy_factory_policy_v3.golden import *
from strategy_factory_policy_v3.graph import compile_graph
from strategy_factory_policy_v3.engine import execute_policy
from strategy_factory_policy_v3.enums import *
from strategy_factory_policy_v3.contracts import OperatorOverride

def run(graph=None,occ=None,out=None,override=None):
    a=golden_admission();m=golden_manual();f=golden_fallback();au=golden_authority();g=graph or golden_hybrid_graph(a,m,f,au); return execute_policy(compile_graph(g,a if g.mode is not PolicyMode.MANUAL_ONLY else None),occ or golden_occurrence(),m,f,au,admission=a if g.mode is not PolicyMode.MANUAL_ONLY else None,model_output=out if out is not None else (golden_output() if g.mode is not PolicyMode.MANUAL_ONLY else None),operator_override=override)
def test_manual_only_exact_parity():
    d=run(golden_manual_graph()); assert d.status is DecisionStatus.APPROVED and d.treatment=='market' and d.risk_tier=='standard'
def test_hybrid_changes_treatment_within_support():
    d=run(); assert d.status is DecisionStatus.APPROVED and d.treatment=='limit'
def test_low_confidence_falls_back_manual():
    d=run(out=replace(golden_output(),uncertainty=.9)); assert d.fallback_used is FallbackAction.MANUAL_ONLY and d.treatment=='market'
def test_missing_model_falls_back_manual():
    a=golden_admission();m=golden_manual();f=golden_fallback();au=golden_authority();g=golden_hybrid_graph(a,m,f,au);d=execute_policy(compile_graph(g,a),golden_occurrence(),m,f,au,admission=a,model_output=None);assert d.fallback_used is FallbackAction.MANUAL_ONLY
def test_manual_veto_beats_model():
    d=run(occ=replace(golden_occurrence(),features={**golden_occurrence().features,'blocked':True})); assert d.status is DecisionStatus.REJECTED and d.decisive_authority is Authority.MANUAL_POLICY
def test_kill_switch_beats_everything():
    g=golden_hybrid_graph(); nodes=tuple(replace(n,config={'engaged':True}) if n.kind is NodeKind.KILL_SWITCH else n for n in g.nodes); d=run(replace(g,nodes=nodes)); assert d.status is DecisionStatus.REJECTED and d.decisive_authority is Authority.KILL_SWITCH
def test_risk_rejection_beats_operator_approval():
    g=golden_hybrid_graph(); nodes=tuple(replace(n,config={'risk_rejected':True}) if n.kind is NodeKind.RISK_GATE else n for n in g.nodes); ov=OperatorOverride('ov:1','occ:1',OverrideKind.APPROVE,'op','reviewed',4000,6000,'a'*64); d=run(replace(g,nodes=nodes),override=ov); assert d.status is DecisionStatus.REJECTED and d.decisive_authority is Authority.RISK_ENGINE
def test_operator_veto_logged():
    ov=OperatorOverride('ov:1','occ:1',OverrideKind.VETO,'op','unsafe',4000,6000,'a'*64); d=run(override=ov); assert d.status is DecisionStatus.REJECTED and d.decisive_authority is Authority.HUMAN_OPERATOR
def test_operator_required_without_override_pending():
    g=golden_hybrid_graph(); nodes=list(g.nodes); idx=next(i for i,n in enumerate(nodes) if n.kind is NodeKind.FALLBACK); nodes.insert(idx,PolicyNodeSpec('approval',NodeKind.OPERATOR_APPROVAL,('kill',),Authority.HUMAN_OPERATOR,{'required':True})); nodes[idx+1]=replace(nodes[idx+1],dependencies=('approval',)); d=run(replace(g,nodes=tuple(nodes))); assert d.status is DecisionStatus.PENDING_APPROVAL
def test_repeated_run_byte_stable(): assert run().decision_hash==run().decision_hash
def test_trace_has_every_node(): assert len(run().trace)==len(golden_hybrid_graph().nodes)
def test_valid_model_filter_can_abstain_without_manual_fallback():
    d=run(out=replace(golden_output(),action_probabilities={'enter_long':.2,'no_action':.8})); assert d.status is DecisionStatus.ABSTAINED and d.fallback_used is None and d.decisive_authority is Authority.MODEL
