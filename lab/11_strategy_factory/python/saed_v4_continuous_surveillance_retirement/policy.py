from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer,number,enum,sorted_unique_strings
from .errors import PolicyError
from .canonical import content_hash,seal
DIRECTIONS={"HIGHER_BAD","LOWER_BAD","ABSOLUTE_BAD"}
SCOPES={"CELL","MODEL","CONTEXT","TREATMENT","FLEET"}
def freeze_policy(v:dict)->dict:
 exact(v,["policy_id","version","metrics","windows","persistence_windows","action_thresholds","minimum_metric_coverage_bps","minimum_window_coverage_bps","retirement_approval_roles","retirement_min_approvals","retirement_requires_replacement","reinstatement_requires_new_qualification","threshold_changes_require_new_version","automatic_live_action_allowed","research_only"])
 metrics=list_of(v["metrics"],"metrics",12);unique(metrics,"metric_id","metrics")
 for m in metrics:
  exact(m,["metric_id","scope","direction","warn_threshold","critical_threshold","weight","minimum_samples","detectors","missing_action","description"])
  enum(m["scope"],SCOPES,"scope");enum(m["direction"],DIRECTIONS,"direction");number(m["warn_threshold"],"warn_threshold");number(m["critical_threshold"],"critical_threshold");number(m["weight"],"weight",0.01,10);integer(m["minimum_samples"],"minimum_samples",1);sorted_unique_strings(m["detectors"],"detectors",1)
  if m["direction"]=="HIGHER_BAD" and m["critical_threshold"]<=m["warn_threshold"]:raise PolicyError("higher-bad thresholds invalid")
  if m["direction"]=="LOWER_BAD" and m["critical_threshold"]>=m["warn_threshold"]:raise PolicyError("lower-bad thresholds invalid")
 windows=list_of(v["windows"],"windows",6);unique(windows,"window_id","windows")
 for x in windows:exact(x,["window_id","ordinal","start_known_time","end_known_time","evidence_role"]);integer(x["ordinal"],"ordinal",0)
 if [x["ordinal"] for x in sorted(windows,key=lambda z:z["ordinal"])]!=list(range(len(windows))):raise PolicyError("window ordinals invalid")
 integer(v["persistence_windows"],"persistence_windows",2,6)
 a=v["action_thresholds"];exact(a,["watch","restrict","quarantine","retire_candidate"])
 vals=[number(a[k],k,0) for k in ["watch","restrict","quarantine","retire_candidate"]]
 if vals!=sorted(vals) or len(set(vals))!=4:raise PolicyError("action thresholds must increase")
 for k in ["minimum_metric_coverage_bps","minimum_window_coverage_bps"]:integer(v[k],k,9000,10000)
 roles=sorted_unique_strings(v["retirement_approval_roles"],"retirement_approval_roles",4);integer(v["retirement_min_approvals"],"retirement_min_approvals",2,len(roles))
 if v["retirement_requires_replacement"] is not True or v["reinstatement_requires_new_qualification"] is not True or v["threshold_changes_require_new_version"] is not True or v["automatic_live_action_allowed"] is not False or v["research_only"] is not True:raise PolicyError("policy boundary invalid")
 x=deepcopy(v);x["metrics"]=sorted(metrics,key=lambda z:z["metric_id"]);x["windows"]=sorted(windows,key=lambda z:z["ordinal"]);x["policy_content_hash"]=content_hash(x);return seal(x,"v441_policy","frozen_policy_id","frozen_policy_hash")
