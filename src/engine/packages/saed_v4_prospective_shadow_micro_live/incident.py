from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer
from .errors import IncidentError
from .canonical import seal,hash_chain

def freeze_runbook(v:dict)->dict:
 exact(v,["runbook_id","version","procedures","kill_switch_default_armed","rollback_target","maximum_detection_seconds","maximum_containment_seconds","research_only"])
 ps=list_of(v["procedures"],"procedures",8);unique(ps,"procedure_id","procedures")
 for p in ps:exact(p,["procedure_id","trigger","severity","immediate_action","owner_role","evidence_required","automatic_action_allowed"])
 if v["kill_switch_default_armed"] is not True or v["rollback_target"]!="OFF" or v["research_only"] is not True:raise IncidentError("runbook boundary invalid")
 integer(v["maximum_detection_seconds"],"maximum_detection_seconds",1,3600);integer(v["maximum_containment_seconds"],"maximum_containment_seconds",1,3600)
 return seal(deepcopy(v),"v439_runbook","frozen_runbook_id","frozen_runbook_hash")
def drill(runbook:dict)->dict:
 scenarios=[("UNAUTHORIZED_ORDER_SIDE_EFFECT","CRITICAL"),("RUNTIME_HASH_MISMATCH","CRITICAL"),("LATENCY_BREACH","HIGH"),("RECONCILIATION_BREAK","CRITICAL"),("BROKER_DISCONNECT","HIGH"),("DAILY_LOSS_CAP","CRITICAL"),("POSITION_DRIFT","CRITICAL"),("CREDENTIAL_EXPOSURE","CRITICAL")]
 events=[]
 for i,(trigger,severity) in enumerate(scenarios):events.append({"scenario_id":f"DRILL{i:02d}","trigger":trigger,"severity":severity,"detected_seconds":1+i,"contained_seconds":3+i,"kill_switch_armed":True,"order_path_disabled":True,"rollback_mode":"OFF","baseline_restored":True,"evidence_complete":True,"synthetic_drill":True,"research_only":True})
 passed=all(x["detected_seconds"]<=runbook["maximum_detection_seconds"] and x["contained_seconds"]<=runbook["maximum_containment_seconds"] and x["baseline_restored"] for x in events)
 return seal({"phase":"SAED_V4_39","events":hash_chain(events,"v439_drill_event"),"scenario_count":len(events),"passed":passed,"actual_live_incident":False,"research_only":True},"v439_drills","drill_bundle_id","drill_bundle_hash")
