from __future__ import annotations
from fp_i02_kernel.enums import PriceSide
from fp_i04_data.enums import MinuteCellState
from .canonical import canonical_sha256,stable_id
from .contracts import HuntFact,MinuteContactObservation
from .enums import ContactState
from .errors import FPI06Error

_PRESENT=(MinuteCellState.PRESENT,MinuteCellState.REVISED)
def _contact(side,bar,price):
    return bar.high>=price if side is PriceSide.HIGH else bar.low<=price
def _extreme(side,bar): return bar.high if side is PriceSide.HIGH else bar.low

def build_hunt_fact(plan,symbol,reference_id,reference_price,row,bar,source_revision_id):
    extreme=_extreme(plan.side,bar)
    material={'side_plan_id':plan.side_plan_id,'instance_id':plan.relation_instance_id,'symbol':symbol,'side':plan.side,'reference_id':reference_id,'reference_price':reference_price,'minute':row.open_utc_ms,'bar_hash':bar.bar_hash,'extreme':extreme,'revision':source_revision_id}
    return HuntFact(stable_id('FPHUNT',material,32),plan.side_plan_id,plan.relation_instance_id,symbol,plan.side,reference_id,reference_price,row.open_utc_ms,bar.bar_hash,extreme,source_revision_id,'FP_HRC_HUNT_CONTACT',canonical_sha256(material))

def observe_minute(plan,row,source_revision_id):
    if row.open_utc_ms<plan.check_start_utc_ms or row.open_utc_ms>=plan.check_end_utc_ms: raise FPI06Error('FP_HRC_ROW_OUTSIDE_CHECK_WINDOW','aligned minute outside side plan')
    if row.left.canonical_symbol!=plan.left_symbol or row.right.canonical_symbol!=plan.right_symbol:
        # Permit pair orientation reversal only by explicit normalization.
        if row.left.canonical_symbol==plan.right_symbol and row.right.canonical_symbol==plan.left_symbol:
            left_cell,right_cell=row.right,row.left
        else: raise FPI06Error('FP_HRC_ROW_SYMBOL_MISMATCH','aligned row symbols do not match plan')
    else:left_cell,right_cell=row.left,row.right
    facts=[]
    if left_cell.state not in _PRESENT or right_cell.state not in _PRESENT:
        state=ContactState.DATA_BLOCKED;reason='FP_HRC_MINUTE_DATA_BLOCKED'
    else:
        lc=_contact(plan.side,left_cell.bar,plan.left_reference_price);rc=_contact(plan.side,right_cell.bar,plan.right_reference_price)
        if lc:facts.append(build_hunt_fact(plan,plan.left_symbol,plan.left_reference_id,plan.left_reference_price,row,left_cell.bar,source_revision_id))
        if rc:facts.append(build_hunt_fact(plan,plan.right_symbol,plan.right_reference_id,plan.right_reference_price,row,right_cell.bar,source_revision_id))
        if lc and rc:state=ContactState.BOTH_SAME_M1;reason='FP_HRC_SYMMETRIC_SAME_M1'
        elif lc:state=ContactState.LEFT_ONLY;reason='FP_HRC_LEFT_CONTACT_ONLY'
        elif rc:state=ContactState.RIGHT_ONLY;reason='FP_HRC_RIGHT_CONTACT_ONLY'
        else:state=ContactState.NONE;reason='FP_HRC_NO_CONTACT'
    left_id=next((f.hunt_fact_id for f in facts if f.canonical_symbol==plan.left_symbol),'')
    right_id=next((f.hunt_fact_id for f in facts if f.canonical_symbol==plan.right_symbol),'')
    material={'plan':plan.side_plan_id,'minute':row.open_utc_ms,'state':state,'left_fact':left_id,'right_fact':right_id,'row':row.row_id,'revision':row.left.source_revision_hash+row.right.source_revision_hash}
    obs=MinuteContactObservation(stable_id('FPCONTACT',material,32),plan.side_plan_id,row.open_utc_ms,state,left_id,right_id,row.row_id,canonical_sha256((row.left.source_revision_hash,row.right.source_revision_hash)),reason,canonical_sha256(material))
    return obs,tuple(facts)
