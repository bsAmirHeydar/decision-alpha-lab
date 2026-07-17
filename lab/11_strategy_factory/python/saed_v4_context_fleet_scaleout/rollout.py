from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer,number,enum
from .errors import RolloutError
from .canonical import seal,hash_chain,content_hash
STAGES={"REGISTERED","CANARY","WAVE_1","WAVE_2","FLEET_REFERENCE","QUARANTINED","ROLLED_BACK"}
def freeze_rollout_policy(v:dict)->dict:
 exact(v,["policy_id","version","waves","minimum_canary_cells","max_concurrent_tenant_rollouts","error_rate_threshold","latency_p99_threshold_ms","reconciliation_delta_threshold","automatic_live_promotion_allowed","rollback_target","research_only"])
 if v["automatic_live_promotion_allowed"] is not False or v["rollback_target"]!="REGISTERED" or v["research_only"] is not True:raise RolloutError("rollout boundary invalid")
 waves=list_of(v["waves"],"waves",4);unique(waves,"wave_id","waves")
 for x in waves:exact(x,["wave_id","ordinal","fraction_bps","minimum_observations","required_gates"]);integer(x["ordinal"],"ordinal",0);integer(x["fraction_bps"],"fraction_bps",1,10000);integer(x["minimum_observations"],"minimum_observations",1)
 if [x["ordinal"] for x in sorted(waves,key=lambda z:z["ordinal"])]!=list(range(len(waves))):raise RolloutError("wave ordinals invalid")
 integer(v["minimum_canary_cells"],"minimum_canary_cells",2);integer(v["max_concurrent_tenant_rollouts"],"max_concurrent_tenant_rollouts",1);number(v["error_rate_threshold"],"error_rate_threshold",0,1);integer(v["latency_p99_threshold_ms"],"latency_p99_threshold_ms",1);number(v["reconciliation_delta_threshold"],"reconciliation_delta_threshold",0)
 return seal(deepcopy(v),"v440_rollout_policy","frozen_policy_id","frozen_policy_hash")
def simulate_rollout(registry:dict,policy:dict,health_samples:list[dict])->dict:
 by_cell={x["cell_id"]:x for x in health_samples};events=[];eligible=[];quarantined=[]
 for c in registry["cells"]:
  s=by_cell.get(c["cell_id"])
  passed=bool(s and s["sample_count"]>=10 and s["error_rate"]<=policy["error_rate_threshold"] and s["latency_p99_ms"]<=policy["latency_p99_threshold_ms"] and abs(s["reconciliation_delta"])<=policy["reconciliation_delta_threshold"] and s["heartbeat_fresh"] is True)
  target="FLEET_REFERENCE" if passed and c["state"]=="QUALIFIED_REFERENCE" else "QUARANTINED"
  (eligible if target=="FLEET_REFERENCE" else quarantined).append(c["cell_id"])
  events.append({"cell_id":c["cell_id"],"from_state":c["state"],"to_state":target,"gates_passed":passed,"manual_live_authorization":False,"live_side_effects_allowed":False,"reason":"REFERENCE_GATES_PASS" if passed else "HEALTH_OR_RECONCILIATION_FAILURE"})
 if len(eligible)<policy["minimum_canary_cells"]:raise RolloutError("insufficient canary capacity")
 return seal({"registry_hash":registry["compiled_registry_hash"],"policy_hash":policy["frozen_policy_hash"],"events":hash_chain(events,"v440_rollout_event"),"eligible_cells":sorted(eligible),"quarantined_cells":sorted(quarantined),"fleet_reference_ready":len(eligible)>0,"automatic_live_promotion":False,"capital_activation_allowed":False,"production_authorized":False,"research_only":True},"v440_rollout","rollout_id","rollout_hash")
