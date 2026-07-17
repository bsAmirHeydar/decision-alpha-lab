from __future__ import annotations
from collections import defaultdict
from .canonical import q,seal,content_hash
ACTIONS=["CONTINUE","WATCH","RESTRICT","QUARANTINE","RETIRE_CANDIDATE"]
def fuse_alerts(detection:dict,registry:dict,policy:dict)->dict:
 by=defaultdict(list)
 for a in detection["alerts"]:by[a["cell_id"]].append(a)
 t=policy["action_thresholds"];rows=[]
 for c in registry["cells"]:
  alerts=sorted(by.get(c["cell_id"],[]),key=lambda x:(x["severity"],x["metric_id"]));score=q(sum(float(x["weighted_score"])*(2.0 if x["severity"]=="CRITICAL" else 1.0) for x in alerts))
  if score>=t["retire_candidate"]:action="RETIRE_CANDIDATE"
  elif score>=t["quarantine"]:action="QUARANTINE"
  elif score>=t["restrict"]:action="RESTRICT"
  elif score>=t["watch"]:action="WATCH"
  else:action="CONTINUE"
  rows.append({"cell_id":c["cell_id"],"tenant_id":c["tenant_id"],"namespace":c["namespace"],"context_id":c["context_id"],"context_version":c["context_version"],"model_generation":c["model_generation"],"score":score,"action":action,"alert_count":len(alerts),"critical_count":sum(x["severity"]=="CRITICAL" for x in alerts),"warning_count":sum(x["severity"]=="WARNING" for x in alerts),"metric_ids":[x["metric_id"] for x in alerts],"decision_trace_hash":content_hash([c["cell_id"],score,action,alerts]),"automatic_live_side_effect":False})
 return seal({"detection_hash":detection["detection_hash"],"rows":rows,"cell_count":len(rows),"action_counts":{a:sum(x["action"]==a for x in rows) for a in ACTIONS},"baseline_preserved":True,"automatic_live_action":False,"research_only":True},"v441_fusion","fusion_id","fusion_hash")
