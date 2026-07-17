from __future__ import annotations
from .canonical import hash_chain,seal,content_hash
from .errors import IncidentError
TRANSITIONS={"DETECTED":{"TRIAGED"},"TRIAGED":{"CONTAINED"},"CONTAINED":{"RESOLVED","PENDING_RETIREMENT"},"RESOLVED":{"CLOSED"}}
def build_incidents(fusion:dict,cutoff:str)->dict:
 events=[];incidents=[]
 for row in fusion["rows"]:
  if row["action"] not in {"RESTRICT","QUARANTINE","RETIRE_CANDIDATE"}:continue
  iid=f"INC_{row['cell_id']}"
  states=["DETECTED","TRIAGED","CONTAINED"]
  terminal="PENDING_RETIREMENT" if row["action"]=="RETIRE_CANDIDATE" else "RESOLVED"
  states.append(terminal)
  previous=None
  for state in states:
   if previous and previous in TRANSITIONS and state not in TRANSITIONS[previous]:raise IncidentError("invalid transition")
   events.append({"incident_id":iid,"cell_id":row["cell_id"],"from_state":previous,"to_state":state,"known_time":cutoff,"action":row["action"],"live_side_effect":False})
   previous=state
  incidents.append({"incident_id":iid,"cell_id":row["cell_id"],"tenant_id":row["tenant_id"],"severity":"CRITICAL" if row["action"] in {"QUARANTINE","RETIRE_CANDIDATE"} else "HIGH","state":terminal,"trigger_action":row["action"],"decision_trace_hash":row["decision_trace_hash"],"owner_role":"SURVEILLANCE_DUTY_OFFICER","known_time":cutoff,"cross_tenant_scope":False})
 return seal({"fusion_hash":fusion["fusion_hash"],"incidents":incidents,"events":hash_chain(events,"v441_incident_event"),"incident_count":len(incidents),"open_count":sum(x["state"]=="PENDING_RETIREMENT" for x in incidents),"cross_tenant_incidents":0,"research_only":True},"v441_incidents","incident_ledger_id","incident_ledger_hash")
