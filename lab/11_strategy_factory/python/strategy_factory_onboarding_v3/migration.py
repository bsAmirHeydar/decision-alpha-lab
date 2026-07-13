from __future__ import annotations
from .contracts import MigrationWavePlan,MigrationWaveReport
from .canonical import stable_id
from .enums import MigrationStatus
def execute_wave(plan:MigrationWavePlan,parity_passed:dict[str,bool],previous_context_ids:tuple[str,...]=())->MigrationWaveReport:
    completed=[];failed=None;stopped=False
    for unit in plan.units:
        if not parity_passed.get(unit.unit_id,False):failed=unit.unit_id;stopped=True;break
        completed.append(unit.unit_id)
        if plan.stop_after_unit==unit.unit_id:stopped=True;break
    unaffected=tuple(sorted(set(previous_context_ids)-{u.context_id for u in plan.units if u.unit_id in completed}))
    return MigrationWaveReport(stable_id('migration-report',{'plan':plan.plan_hash,'completed':completed,'failed':failed}),'1.0.0',plan.plan_hash,tuple(completed),stopped,failed,unaffected,True)
