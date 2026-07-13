import pytest
from fp_i02_kernel.enums import Direction,RelationCode
from fp_i08_weekly.stack import resolve_active_stack
from fp_i08_weekly.gate import evaluate_direction_gate
from fp_i08_weekly.store import build_snapshot,upsert_context
from fp_i08_weekly.checkpoint import create_checkpoint,validate_checkpoint
from fp_i08_weekly.enums import WWDataState,WWLifecycleState
from fp_i08_weekly.errors import FPI08Error
from helpers import config,context

def test_snapshot_and_checkpoint_parity():
 c=context();s=resolve_active_stack(config().pair_id,(c,),WWDataState.COMPLETE,1_000_080_000,config());g=evaluate_direction_gate('S',RelationCode.AL,Direction.BULLISH,s,1_000_080_000);snap=build_snapshot(config(),(c,),(),s,(g,),'REV',1_000_080_000);cp=create_checkpoint(snap);assert validate_checkpoint(cp,snap)
def test_checkpoint_rejects_changed_snapshot():
 c=context();s=resolve_active_stack(config().pair_id,(c,),WWDataState.COMPLETE,1_000_080_000,config());snap=build_snapshot(config(),(c,),(),s,(),'REV',1_000_080_000);cp=create_checkpoint(snap);s2=resolve_active_stack(config().pair_id,(),WWDataState.COMPLETE,1_000_080_000,config());snap2=build_snapshot(config(),(),(),s2,(),'REV',1_000_080_000)
 with pytest.raises(FPI08Error):validate_checkpoint(cp,snap2)
def test_upsert_replaces_context():
 c=context();n=context(state=WWLifecycleState.NEUTRALIZED);out=upsert_context((c,),n);assert len(out)==1 and out[0].state is WWLifecycleState.NEUTRALIZED
