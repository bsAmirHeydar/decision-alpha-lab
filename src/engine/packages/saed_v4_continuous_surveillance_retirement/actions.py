from __future__ import annotations
from .canonical import hash_chain,seal,content_hash
from .errors import ActionError
ACTION_EFFECT={"CONTINUE":"NO_CHANGE","WATCH":"INCREASE_OBSERVATION","RESTRICT":"DISABLE_NEW_REFERENCE_ROUTES","QUARANTINE":"REMOVE_FROM_REFERENCE_ROUTING","RETIRE_CANDIDATE":"FREEZE_AND_ESCALATE_RETIREMENT_REVIEW"}
def compile_actions(fusion:dict,registry:dict,cutoff:str)->dict:
 cells={x["cell_id"]:x for x in registry["cells"]};events=[];rows=[]
 for d in fusion["rows"]:
  c=cells[d["cell_id"]];action=d["action"]
  if d["tenant_id"]!=c["tenant_id"] or d["namespace"]!=c["namespace"]:raise ActionError("cross-boundary action")
  state={"CONTINUE":"QUALIFIED_REFERENCE","WATCH":"QUALIFIED_REFERENCE_WATCH","RESTRICT":"RESTRICTED_REFERENCE","QUARANTINE":"QUARANTINED","RETIRE_CANDIDATE":"FROZEN_RETIREMENT_REVIEW"}[action]
  row={"action_id":f"ACT_{c['cell_id']}","cell_id":c["cell_id"],"tenant_id":c["tenant_id"],"namespace":c["namespace"],"decision":action,"effect":ACTION_EFFECT[action],"target_state":state,"known_time":cutoff,"automatic_live_side_effect":False,"capital_effect":0.0,"order_effect":0,"baseline_preserved":True,"approved_scope":"SYNTHETIC_REFERENCE_ONLY"}
  rows.append(row);events.append(row)
 return seal({"fusion_hash":fusion["fusion_hash"],"rows":rows,"events":hash_chain(events,"v441_action_event"),"action_count":len(rows),"live_order_side_effects":0,"capital_delta":0.0,"cross_tenant_actions":0,"baseline_preserved":True,"research_only":True},"v441_actions","action_ledger_id","action_ledger_hash")
