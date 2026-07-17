from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer,enum
from .errors import ModeError
from .canonical import content_hash,seal
MODES={"OFF","PAPER","SHADOW","MICRO_LIVE_QUALIFICATION","MICRO_LIVE","PRODUCTION"}
def freeze_mode_ladder(v:dict)->dict:
 exact(v,["ladder_id","version","stages","initial_mode","automatic_transition_allowed","regression_allowed","research_only"])
 if v["initial_mode"]!="OFF" or v["automatic_transition_allowed"] is not False or v["regression_allowed"] is not True or v["research_only"] is not True:raise ModeError("mode ladder boundary invalid")
 stages=list_of(v["stages"],"stages",6);unique(stages,"stage_id","stages");out=[]
 for s in stages:
  exact(s,["stage_id","ordinal","mode","required_gates","side_effects_allowed","capital_allowed","manual_authorization_required","rollback_mode"]);integer(s["ordinal"],"ordinal",0);enum(s["mode"],MODES,"mode")
  if s["mode"] in {"OFF","PAPER","SHADOW","MICRO_LIVE_QUALIFICATION"} and (s["side_effects_allowed"] is not False or s["capital_allowed"] is not False):raise ModeError("pre-live mode cannot have side effects")
  if s["mode"] in {"MICRO_LIVE","PRODUCTION"} and s["manual_authorization_required"] is not True:raise ModeError("live mode requires manual authorization")
  out.append(deepcopy(s))
 out=sorted(out,key=lambda z:z["ordinal"])
 if [x["ordinal"] for x in out]!=list(range(len(out))):raise ModeError("stage ordinals invalid")
 x=deepcopy(v);x["stages"]=out;x["ladder_hash"]=content_hash(out);return seal(x,"v439_ladder","frozen_ladder_id","frozen_ladder_hash")
def transition(current:str,target:str,ladder:dict,passed_gates:set[str],manual_authorized:bool)->dict:
 stages={x["mode"]:x for x in ladder["stages"]}
 if current not in stages or target not in stages:raise ModeError("unknown mode")
 cur=stages[current];tar=stages[target]
 if tar["ordinal"]>cur["ordinal"]+1:raise ModeError("cannot skip stages")
 if tar["ordinal"]<cur["ordinal"] and target!=cur["rollback_mode"]:raise ModeError("invalid rollback")
 missing=sorted(set(tar["required_gates"])-passed_gates)
 if missing:raise ModeError(f"missing gates {missing}")
 if tar["manual_authorization_required"] and not manual_authorized:raise ModeError("manual authorization missing")
 return seal({"from_mode":current,"to_mode":target,"passed_gates":sorted(passed_gates),"manual_authorized":manual_authorized,"side_effects_allowed":tar["side_effects_allowed"],"capital_allowed":tar["capital_allowed"],"research_only":True},"v439_transition","transition_id","transition_hash")
