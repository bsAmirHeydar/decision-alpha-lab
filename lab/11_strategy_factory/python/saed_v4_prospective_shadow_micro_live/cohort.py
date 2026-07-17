from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer,sorted_unique_strings,enum
from .errors import CohortError
from .canonical import content_hash,seal
ROLES={"TRAIN","VALIDATION","HIDDEN_EVALUATION","PROSPECTIVE_PAPER","SHADOW","MICRO_LIVE_QUALIFICATION"}
def freeze_cohort(v:dict)->dict:
 exact(v,["cohort_id","version","frozen_at","prospective_start","prospective_end","cutoff_time","contexts","instruments","data_roles","minimum_observations","maximum_observations","decision_frequency","outcome_fields_visible_at_freeze","selection_locked","research_only"])
 if not (v["frozen_at"]<v["prospective_start"]<v["prospective_end"]<=v["cutoff_time"]):raise CohortError("prospective chronology invalid")
 if v["outcome_fields_visible_at_freeze"]!=[]:raise CohortError("future outcomes visible at freeze")
 if v["selection_locked"] is not True or v["research_only"] is not True:raise CohortError("cohort must be locked research-only")
 sorted_unique_strings(v["contexts"],"contexts",1);sorted_unique_strings(v["instruments"],"instruments",1)
 roles=list_of(v["data_roles"],"data_roles",3);unique(roles,"role_id","data_roles")
 for r in roles:
  exact(r,["role_id","role","start","end","mutable"]);enum(r["role"],ROLES,"role");
  if r["start"]>=r["end"] or r["mutable"] is not False:raise CohortError("data role invalid")
 integer(v["minimum_observations"],"minimum_observations",20);integer(v["maximum_observations"],"maximum_observations",v["minimum_observations"])
 if v["decision_frequency"]!="BAR_CLOSE":raise CohortError("bar-close decisions required")
 x=deepcopy(v);x["cohort_hash"]=content_hash(x);return seal(x,"v439_cohort","frozen_cohort_id","frozen_cohort_hash")

def validate_observations(rows:list[dict],cohort:dict)->dict:
 if not isinstance(rows,list):raise CohortError("observations must be list")
 seen=set();prev=""
 for r in rows:
  exact(r,["observation_id","known_time","context_id","instrument","decision","side","signal_score","expected_edge_bps","expected_cost_bps","bid","ask","bar_high","bar_low","next_bid","next_ask","latency_ms","baseline_decision","synthetic_fixture"])
  if r["observation_id"] in seen:raise CohortError("duplicate observation")
  if not (cohort["prospective_start"]<=r["known_time"]<=cohort["prospective_end"]):raise CohortError("observation outside prospective window")
  if prev and r["known_time"]<prev:raise CohortError("observations out of order")
  if r["context_id"] not in cohort["contexts"] or r["instrument"] not in cohort["instruments"]:raise CohortError("unfrozen context or instrument")
  if r["synthetic_fixture"] is not True:raise CohortError("reference accepts synthetic fixtures only")
  seen.add(r["observation_id"]);prev=r["known_time"]
 if len(rows)<cohort["minimum_observations"] or len(rows)>cohort["maximum_observations"]:raise CohortError("observation budget violated")
 return seal({"phase":"SAED_V4_39","cohort_hash":cohort["frozen_cohort_hash"],"observation_count":len(rows),"first_known_time":rows[0]["known_time"],"last_known_time":rows[-1]["known_time"],"future_suffix_used":False,"validated":True,"research_only":True},"v439_observations","receipt_id","receipt_hash")
