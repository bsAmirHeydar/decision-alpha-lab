from __future__ import annotations
from .canonical import seal,hash_chain,content_hash
from .errors import AuthorityError
def build_control_plane_journal(manifest:dict,rollout:dict,commands:list[dict])->dict:
 allowed={"REGISTER","PLACE","ROUTE_ENABLE","CANARY","QUARANTINE","ROLLBACK","RETIRE","NOOP"};seen=set();events=[]
 cell_ids={x["cell_id"] for x in manifest["cells"]}
 for c in sorted(commands,key=lambda x:(x["known_time"],x["command_id"])):
  if set(c)!={"command_id","known_time","actor_role","tenant_id","cell_id","action","idempotency_key","approved","synthetic_fixture"}:raise AuthorityError("command contract invalid")
  if c["action"] not in allowed or c["cell_id"] not in cell_ids:raise AuthorityError("command invalid")
  if c["idempotency_key"] in seen:continue
  if c["action"] in {"CANARY","ROUTE_ENABLE"} and c["approved"] is not True:raise AuthorityError("approval required")
  if c["synthetic_fixture"] is not True:raise AuthorityError("reference commands must be synthetic")
  seen.add(c["idempotency_key"]);events.append({**c,"accepted":True,"side_effect_scope":"REFERENCE_CONTROL_PLANE_ONLY","live_order_side_effect":False})
 return seal({"fleet_manifest_hash":manifest["fleet_manifest_hash"],"rollout_hash":rollout["rollout_hash"],"events":hash_chain(events,"v440_control_event"),"accepted_count":len(events),"deduplicated_count":len(commands)-len(events),"idempotent":True,"live_order_side_effects":0,"research_only":True},"v440_control_journal","journal_id","journal_hash")
