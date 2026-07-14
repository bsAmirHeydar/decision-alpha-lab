from .contracts import *
from .plan import build_plan
from .canonical import stable_id

def revalidate_plan(prior,proof,winner,readiness,quote,spec,risk,now):
    new=build_plan(proof,winner,readiness,quote,spec,risk,now,prior.plan_id,prior.revision+1)
    if new.state!=PlanState.READY:
        return RevalidationResult(RevalidationDisposition.BLOCKED,prior.plan_id,new,new.reason_codes,stable_id("FPREVAL",{"prior":prior.plan_id,"new":new.plan_id,"status":"BLOCKED"}))
    same=prior.geometry.geometry_hash==new.geometry.geometry_hash and prior.sizing.sizing_hash==new.sizing.sizing_hash
    disp=RevalidationDisposition.UNCHANGED if same else RevalidationDisposition.REPRICED
    return RevalidationResult(disp,prior.plan_id,new,(),stable_id("FPREVAL",{"prior":prior.plan_id,"new":new.plan_id,"status":disp}))
