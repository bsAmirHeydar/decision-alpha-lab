from .contracts import *
def reconcile_risk(plan:ExecutionPlan,position:PaperPosition|None,spec:SymbolSpec):
    if position is None: return {"status":"NO_POSITION","planned_max_loss":plan.sizing.estimated_max_loss,"actual_initial_max_loss":0.0,"within_cap":True}
    distance=abs(position.average_entry-position.stop)
    loss=(distance/spec.tick_size)*spec.tick_value_loss_per_lot*position.volume
    return {"status":"RECONCILED","planned_max_loss":plan.sizing.estimated_max_loss,"actual_initial_max_loss":loss,"risk_budget":plan.sizing.risk_budget,"within_cap":loss<=plan.sizing.risk_budget+1e-8,"risk_delta":loss-plan.sizing.estimated_max_loss}
