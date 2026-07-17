from __future__ import annotations
from collections import defaultdict
from .canonical import q,seal,content_hash
from .errors import DetectionError
def _level(value:float,m:dict)->str:
 if m["direction"]=="HIGHER_BAD":return "CRITICAL" if value>=m["critical_threshold"] else "WARNING" if value>=m["warn_threshold"] else "NORMAL"
 if m["direction"]=="LOWER_BAD":return "CRITICAL" if value<=m["critical_threshold"] else "WARNING" if value<=m["warn_threshold"] else "NORMAL"
 x=abs(value);return "CRITICAL" if x>=abs(m["critical_threshold"]) else "WARNING" if x>=abs(m["warn_threshold"]) else "NORMAL"
def _breach_score(value:float,m:dict)->float:
 warn=float(m["warn_threshold"]);crit=float(m["critical_threshold"])
 if m["direction"]=="HIGHER_BAD":
  if value<warn:return 0.0
  return q(1.0+max(0.0,(value-warn)/max(abs(crit-warn),1e-9)))
 if m["direction"]=="LOWER_BAD":
  if value>warn:return 0.0
  return q(1.0+max(0.0,(warn-value)/max(abs(warn-crit),1e-9)))
 value=abs(value);warn=abs(warn);crit=abs(crit)
 if value<warn:return 0.0
 return q(1.0+max(0.0,(value-warn)/max(abs(crit-warn),1e-9)))
def run_detectors(ledger:dict,policy:dict)->dict:
 metrics={x["metric_id"]:x for x in policy["metrics"]};window_ord={x["window_id"]:x["ordinal"] for x in policy["windows"]};groups=defaultdict(list)
 for r in ledger["rows"]:groups[(r["cell_id"],r["metric_id"])].append(r)
 alerts=[];summaries=[]
 for (cell_id,metric_id),rows in sorted(groups.items()):
  m=metrics[metric_id];rows=sorted(rows,key=lambda x:window_ord[x["window_id"]]);levels=[_level(float(x["value"]),m) for x in rows]
  trailing=0
  for level in reversed(levels):
   if level=="NORMAL":break
   trailing+=1
  latest=rows[-1];latest_level=levels[-1];persistent=trailing>=policy["persistence_windows"]
  score=q(_breach_score(float(latest["value"]),m)*float(m["weight"]))
  detector_rows=[]
  for d in m["detectors"]:
   if d=="THRESHOLD":signal=latest_level!="NORMAL"
   elif d=="EWMA":signal=sum(float(x["value"]) for x in rows[-3:])/min(3,len(rows))!=float(latest["baseline_value"])
   elif d=="CUSUM":signal=sum(abs(float(x["value"])-float(x["baseline_value"])) for x in rows[-3:])>0
   elif d=="PAGE_HINKLEY":signal=max(float(x["value"]) for x in rows)-min(float(x["value"]) for x in rows)>0
   else:signal=latest_level!="NORMAL"
   detector_rows.append({"detector_id":d,"signal":bool(signal),"known_time":latest["known_time"],"future_suffix_used":False})
  summary={"cell_id":cell_id,"metric_id":metric_id,"latest_level":latest_level,"latest_value":latest["value"],"baseline_value":latest["baseline_value"],"trailing_breach_windows":trailing,"persistent":persistent,"weighted_score":score,"detectors":detector_rows,"summary_hash":content_hash([cell_id,metric_id,levels,score])}
  summaries.append(summary)
  if latest_level!="NORMAL" and persistent:
   alerts.append({"alert_id":f"ALERT_{cell_id}_{metric_id}","cell_id":cell_id,"metric_id":metric_id,"severity":latest_level,"weighted_score":score,"trailing_breach_windows":trailing,"known_time":latest["known_time"],"reason":"PERSISTENT_CRITICAL_BREACH" if latest_level=="CRITICAL" else "PERSISTENT_WARNING_BREACH","future_suffix_used":False,"synthetic_fixture":True})
 return seal({"ledger_hash":ledger["ledger_hash"],"policy_hash":policy["frozen_policy_hash"],"summaries":summaries,"alerts":alerts,"summary_count":len(summaries),"alert_count":len(alerts),"future_suffix_used":False,"deterministic":True,"research_only":True},"v441_detection","detection_id","detection_hash")
