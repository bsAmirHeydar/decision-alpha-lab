from fp_i02_kernel.enums import Direction,RelationCode,PriceSide
from fp_i08_weekly.stack import resolve_active_stack
from fp_i08_weekly.gate import evaluate_direction_gate
from fp_i08_weekly.enums import WWDataState,GateEligibility
from helpers import config,context

def test_aligned_direction_allowed():
 s=resolve_active_stack(config().pair_id,(context(),),WWDataState.COMPLETE,1_000_080_000,config());d=evaluate_direction_gate('S1',RelationCode.AL,Direction.BULLISH,s,1_000_080_000);assert d.eligibility is GateEligibility.ALLOWED
def test_opposite_direction_suppressed_not_deleted():
 s=resolve_active_stack(config().pair_id,(context(),),WWDataState.COMPLETE,1_000_080_000,config());d=evaluate_direction_gate('S2',RelationCode.AN,Direction.BEARISH,s,1_000_080_000);assert d.eligibility is GateEligibility.SUPPRESSED and d.reason_code=='FP_RC_SUPPRESSED_BY_WW' and d.subject_signal_id=='S2'
def test_no_active_allows_both():
 s=resolve_active_stack(config().pair_id,(),WWDataState.COMPLETE,1_000_080_000,config());assert evaluate_direction_gate('S',RelationCode.NN,Direction.BEARISH,s,1_000_080_000).eligibility is GateEligibility.ALLOWED
def test_incomplete_data_blocks():
 s=resolve_active_stack(config().pair_id,(),WWDataState.INCOMPLETE,1_000_080_000,config());assert evaluate_direction_gate('S',RelationCode.NL,Direction.BULLISH,s,1_000_080_000).eligibility is GateEligibility.BLOCKED
def test_ww_direct_setup_not_self_gated():
 s=resolve_active_stack(config().pair_id,(context(),),WWDataState.COMPLETE,1_000_080_000,config());d=evaluate_direction_gate('WW',RelationCode.WW,Direction.BEARISH,s,1_000_080_000);assert d.eligibility is GateEligibility.NOT_APPLICABLE
