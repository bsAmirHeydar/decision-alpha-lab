from __future__ import annotations
from .canonical import content_hash,stable_id
from .integrity import build_receipt

def build_v4_09_handoff(cube)->dict:
    receipt=build_receipt(cube)
    payload={'phase':'SAED_V4_08','next_phase':'SAED_V4_09','authority':{'read_frozen_outcome_cube':True,'read_path_events':True,'read_cost_breakdowns':True,'build_execution_digital_twin':True,'mutate_outcome_cube':False,'rank_treatments':False,'select_treatment':False,'allocate_risk':False,'activate_runtime':False,'send_order':False,'use_future_information_at_decision_time':False},'cube_id':cube.cube_id,'cube_hash':cube.cube_hash,'integrity_receipt_hash':receipt['receipt_hash'],'complete_exposure':cube.complete_exposure,'evidence_role':cube.evidence_role,'known_as_of':cube.known_as_of,'limitations':['V4-09 must preserve every row and path identity.','Execution digital twin calibration must not retroactively mutate V4-08 outcomes.','No runtime or capital authority is transferred.']}
    payload['handoff_id']=stable_id('v408to09',payload);payload['handoff_hash']=content_hash(payload);return payload
