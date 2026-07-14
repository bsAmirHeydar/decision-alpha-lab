from fp_i10_indicator.scheduler import *
from fp_i10_indicator.enums import *

def test_noop_same_cursor():
 c=IncrementalCursor(60000); p=plan_incremental(cursor=c,target_closed_m1=60000,max_minutes=10,trigger=ProcessTrigger.CALCULATE); assert p.work_minutes==0 and p.mode is WorkMode.NOOP
def test_incremental_one_minute():
 c=IncrementalCursor(60000); p=plan_incremental(cursor=c,target_closed_m1=120000,max_minutes=10,trigger=ProcessTrigger.CALCULATE); assert p.work_minutes==1 and p.end_m1==120000
def test_chunked_catchup():
 c=IncrementalCursor(60000); p=plan_incremental(cursor=c,target_closed_m1=660000,max_minutes=3,trigger=ProcessTrigger.CALCULATE); assert p.mode is WorkMode.CHUNKED_CATCHUP and p.work_minutes==3 and p.remaining_minutes==7
def test_initial_backfill():
 c=IncrementalCursor(0); p=plan_incremental(cursor=c,target_closed_m1=600000,max_minutes=20,trigger=ProcessTrigger.INIT,initial_history_start_m1=60000); assert p.mode is WorkMode.INITIAL_BACKFILL and p.work_minutes==10
def test_apply_plan_updates_cursor():
 c=IncrementalCursor(60000); p=plan_incremental(cursor=c,target_closed_m1=180000,max_minutes=10,trigger=ProcessTrigger.CALCULATE); apply_plan(c,p); assert c.last_processed_m1==180000
