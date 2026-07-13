from dataclasses import replace
from fp_i04_data.backfill import plan_backfill
from fp_i04_data.contracts import GapInterval
from fp_i04_data.enums import BackfillAction,GapReason
from fp_i04_data.golden import golden_config

def gap(reason=GapReason.SOURCE_MISSING,minutes=2):
    return GapInterval('ES',60_000,60_000+minutes*60_000,minutes,reason,'R','0'*64)

def test_normal_gap_plans_bounded_fetch():
    assert plan_backfill((gap(),),golden_config())[0].action is BackfillAction.FETCH_RANGE

def test_large_gap_plans_full_rebuild():
    cfg=replace(golden_config(),maximum_backfill_minutes=1)
    assert plan_backfill((gap(minutes=2),),cfg)[0].action is BackfillAction.FULL_REBUILD

def test_conflict_blocks_backfill():
    assert plan_backfill((gap(GapReason.DUPLICATE_CONFLICT),),golden_config())[0].action is BackfillAction.BLOCK

def test_backfill_order_is_deterministic():
    a=gap();b=GapInterval('NQ',0,60_000,1,GapReason.SOURCE_MISSING,'R','0'*64)
    assert plan_backfill((a,b),golden_config())==plan_backfill((b,a),golden_config())
