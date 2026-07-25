from fp_i02_kernel.enums import Direction,PriceSide
from fp_i08_weekly.stack import resolve_active_stack
from fp_i08_weekly.enums import WWDataState,WWStackDisposition,WWLifecycleState
from helpers import config,context

def test_no_active_complete_allows_both():
 s=resolve_active_stack(config().pair_id,(),WWDataState.COMPLETE,1_000_020_000,config());assert s.active_direction is None and s.reason_code=='FP_RC_WW_NONE_ALLOW_BOTH'
def test_incomplete_data_blocks_without_active(): assert resolve_active_stack(config().pair_id,(),WWDataState.INCOMPLETE,1_000_020_000,config()).reason_code=='FP_RC_WW_DATA_INCOMPLETE'
def test_newest_active_wins():
 a=context(1,Direction.BULLISH,PriceSide.LOW,1_000_020_000);b=context(2,Direction.BEARISH,PriceSide.HIGH,1_000_140_000)
 s=resolve_active_stack(config().pair_id,(a,b),WWDataState.COMPLETE,1_000_200_000,config());assert s.active_ww_context_id==b.ww_context_id and s.active_direction is Direction.BEARISH
 assert [e.disposition for e in s.entries].count(WWStackDisposition.ACTIVE_WINNER)==1
 assert any(e.ww_context_id==a.ww_context_id and e.disposition is WWStackDisposition.ACTIVE_SHADOWED for e in s.entries)
def test_neutralized_newer_does_not_win():
 a=context(1,Direction.BULLISH,confirmed=1_000_020_000);b=context(2,Direction.BEARISH,PriceSide.HIGH,1_000_140_000,WWLifecycleState.NEUTRALIZED)
 s=resolve_active_stack(config().pair_id,(a,b),WWDataState.COMPLETE,1_000_200_000,config());assert s.active_ww_context_id==a.ww_context_id
def test_expired_by_clock_not_active():
 a=context(1,week_end=1_000_080_000);s=resolve_active_stack(config().pair_id,(a,),WWDataState.COMPLETE,1_000_140_000,config());assert not s.active_ww_context_id
