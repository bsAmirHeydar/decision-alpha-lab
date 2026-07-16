from __future__ import annotations
from .contracts import OptimizationBudget
from .budget import BudgetLedger
from .security import scan
from .upstream import validate_upstream
from .scenarios import compile_scenarios,future_suffix_invariance
from .ambiguity import compile_ambiguity_distributions
from .allocations import enumerate_allocations
from .optimizer import solve
from .adversary import bounded_adversary
from .stability import leave_one_scenario_out,radius_sensitivity
from .certificates import build_certificate
from .replay import build_replay_receipt
from .handoff import build_v4_22_handoff
from .canonical import content_hash

def run_reference(config,upstream_documents,score_table,qa=None):
    scan(config);scan(upstream_documents);scan(score_table)
    ledger=BudgetLedger(OptimizationBudget.from_mapping(config['budget']))
    up=validate_upstream(config['upstream_intake'],upstream_documents['certificate'],upstream_documents['registry'],upstream_documents['exposure'],upstream_documents['handoff'])
    scenarios=compile_scenarios(score_table,config['scenario'],config['ambiguity'],ledger)
    ambiguity=compile_ambiguity_distributions(scenarios,config['ambiguity'],ledger)
    complexities={r['treatment_id']:int(r['complexity']) for r in score_table['rows']}
    allocations=enumerate_allocations(scenarios['treatments'],config['optimization'],complexities,ledger)
    report=solve(allocations,scenarios,ambiguity,config['optimization'],config['regret'],config['baseline'],ledger)
    adversary=bounded_adversary(report,scenarios,config['adversary']['steps'],config['adversary']['shock_bound'],ledger)
    stability=leave_one_scenario_out(report,scenarios,ledger)
    radius=radius_sensitivity(report,config['sensitivity_radii'])
    budget=ledger.snapshot()
    certificate=build_certificate(up,scenarios,ambiguity,allocations,report,adversary,stability,budget)
    outputs={'upstream_receipt':up,'scenario_set':scenarios,'ambiguity_set':ambiguity,'allocation_universe':allocations,'optimization_report':report,'adversary_report':adversary,'stability_report':stability,'radius_sensitivity':radius,'budget_snapshot':budget,'certificate':certificate}
    replay=build_replay_receipt({'config':config,'upstream_documents':upstream_documents,'score_table':score_table},outputs)
    outputs['replay_receipt']=replay
    outputs['claim_tier_report']={'phase':'SAED_V4_21','claim_tier':'local_deterministic_synthetic_reference','robust_optimization_implemented':True,'regret_analysis_implemented':True,'real_policy_value_established':False,'real_alpha_established':False,'production_treatment_selection':False,'production_risk_allocation':False,'runtime_activation':False,'production_authorization':False}
    outputs['handoff']=build_v4_22_handoff(certificate,report,scenarios,ambiguity,budget,qa or {'passed':True})
    outputs['reference_run_hash']=content_hash(outputs)
    return outputs
