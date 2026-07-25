from __future__ import annotations
from .contracts import PortfolioRuntimeBundle
from .enums import RuntimeState,ValidationStatus,AllocationStatus
from .errors import PortfolioError

def compile_runtime_bundle(plan,limits,model,validation,ledger,state=RuntimeState.SHADOW):
    if plan.status is not AllocationStatus.ALLOCATED: raise PortfolioError('unallocatable_plan','runtime requires allocated plan')
    if validation.status is not ValidationStatus.PASS: raise PortfolioError('validation_not_passed','runtime requires passed validation')
    if len(set(x.context_id for x in plan.selected))<limits.min_context_count: raise PortfolioError('insufficient_contexts','runtime requires minimum context count')
    return PortfolioRuntimeBundle(bundle_id='portfolio-runtime:'+plan.plan_id,version='1.0.0',plan_hash=plan.plan_hash,limits_hash=limits.limits_hash,dependence_hash=model.model_hash,validation_hash=validation.report_hash,reservation_ledger_hash=ledger.ledger_hash,state=state,context_ids=tuple(sorted(set(x.context_id for x in plan.selected))),order_authority=False,broker_authority=False,network_authority=False,kill_switch_required=True)
