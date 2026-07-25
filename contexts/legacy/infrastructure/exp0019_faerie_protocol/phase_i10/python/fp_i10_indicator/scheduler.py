from dataclasses import dataclass
from .contracts import IncrementalPlan
from .enums import WorkMode,ProcessTrigger
from .canonical import canonical_sha256,stable_id,require_m1

@dataclass(slots=True)
class IncrementalCursor:
    last_processed_m1:int
    def __post_init__(self): require_m1(self.last_processed_m1,'last_processed_m1')

def plan_incremental(*,cursor:IncrementalCursor,target_closed_m1:int,max_minutes:int,trigger:ProcessTrigger,initial_history_start_m1:int|None=None,rebuild=False)->IncrementalPlan:
    require_m1(target_closed_m1,'target_closed_m1')
    if initial_history_start_m1 is not None: require_m1(initial_history_start_m1,'initial_history_start_m1')
    if rebuild:
        start=initial_history_start_m1 if initial_history_start_m1 is not None else cursor.last_processed_m1
        mode=WorkMode.REBUILD
    elif initial_history_start_m1 is not None and cursor.last_processed_m1==0:
        start=initial_history_start_m1; mode=WorkMode.INITIAL_BACKFILL
    else:
        start=cursor.last_processed_m1+60000 if cursor.last_processed_m1 else target_closed_m1
        mode=WorkMode.INCREMENTAL
    if target_closed_m1<start:
        start=target_closed_m1; end=target_closed_m1; work=0; remaining=0; mode=WorkMode.NOOP
    else:
        total=((target_closed_m1-start)//60000)+1
        work=min(total,max_minutes)
        end=start+(work-1)*60000 if work else start
        remaining=max(0,total-work)
        if remaining and mode is WorkMode.INCREMENTAL: mode=WorkMode.CHUNKED_CATCHUP
    reasons=()
    if remaining: reasons=('FP_IND_INCREMENTAL_CHUNK_REMAINING',)
    payload={'mode':mode.value,'start_m1':start,'end_m1':end,'work_minutes':work,'remaining_minutes':remaining,'trigger':trigger.value,'reason_codes':reasons}
    return IncrementalPlan(stable_id('FPPLAN',payload),mode,start,end,work,remaining,trigger,reasons,canonical_sha256(payload))

def apply_plan(cursor:IncrementalCursor,plan:IncrementalPlan):
    if plan.work_minutes: cursor.last_processed_m1=plan.end_m1
    return cursor
