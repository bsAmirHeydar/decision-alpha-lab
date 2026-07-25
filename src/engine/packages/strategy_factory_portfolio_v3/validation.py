from __future__ import annotations
from .contracts import PortfolioValidationReport
from .enums import ValidationStatus

def validate_portfolio(plan,stress_results,standalone_attribution,out_of_sample=True,nested_selection=True):
    combined=sum(x.adjusted_score for x in plan.selected);standalone=sum(standalone_attribution.values());interaction=combined-standalone
    total=max(plan.total_risk,1e-12);concentration=max((sum(x.allocated_risk for x in plan.selected if x.context_id==c) for c in set(x.context_id for x in plan.selected)),default=0)/total
    context_drop_safe=all(x.safe for x in stress_results if 'drop' in x.scenario_id)
    correlation_safe=all(x.safe for x in stress_results if 'corr' in x.scenario_id)
    status=ValidationStatus.PASS if out_of_sample and nested_selection and context_drop_safe and correlation_safe and plan.context_count>=2 else ValidationStatus.FAIL
    limitations=() if status is ValidationStatus.PASS else ('portfolio_activation_requires_two_promoted_contexts_and_stress_pass',)
    return PortfolioValidationReport('validation:'+plan.plan_id,'1.0.0',plan.plan_hash,status,out_of_sample,nested_selection,dict(standalone_attribution),combined,interaction,plan.turnover_cost,max((x.stressed_drawdown for x in stress_results),default=0),max((x.stressed_drawdown for x in stress_results),default=0),concentration,min(1.0,plan.total_risk/max(plan.gross_exposure,1e-12)),tuple(stress_results),context_drop_safe,correlation_safe,limitations)
