from fp_i02_kernel.enums import Direction,PriceSide
from fp_i08_weekly.stack import resolve_active_stack
from fp_i08_weekly.enums import WWDataState
from helpers import config,context

def test_stack_input_order_invariant():
 a=context(1);b=context(2,Direction.BEARISH,PriceSide.HIGH,1_000_140_000)
 assert resolve_active_stack(config().pair_id,(a,b),WWDataState.COMPLETE,1_000_200_000,config()).stack_hash==resolve_active_stack(config().pair_id,(b,a),WWDataState.COMPLETE,1_000_200_000,config()).stack_hash
def test_tie_breaker_signal_id_deterministic():
 a=context(1);b=context(2,Direction.BEARISH,PriceSide.HIGH,1_000_020_000)
 s=resolve_active_stack(config().pair_id,(a,b),WWDataState.COMPLETE,1_000_080_000,config());expected=max((a,b),key=lambda c:(c.confirmed_utc_ms,c.source_signal.signal_id,c.ww_context_id));assert s.active_ww_context_id==expected.ww_context_id
def test_context_identity_changes_by_direction(): assert context(1).context_hash!=context(1,Direction.BEARISH,PriceSide.HIGH).context_hash
