from __future__ import annotations
from copy import deepcopy
from .contracts import exact,integer,number
from .errors import ObservationError
from .canonical import content_hash,hash_chain,seal
def compile_observations(rows:list[dict],registry:dict,policy:dict,cutoff:str)->dict:
 cells={x["cell_id"]:x for x in registry["cells"]};metrics={x["metric_id"]:x for x in policy["metrics"]};windows={x["window_id"]:x for x in policy["windows"]};seen=set();out=[]
 for r in rows:
  exact(r,["observation_id","cell_id","tenant_id","namespace","metric_id","window_id","known_time","sample_count","value","baseline_value","source_hash","evidence_role","future_suffix_used","synthetic_fixture"])
  c=cells.get(r["cell_id"])
  if not c or r["tenant_id"]!=c["tenant_id"] or r["namespace"]!=c["namespace"]:raise ObservationError("cell/tenant/namespace mismatch")
  if r["metric_id"] not in metrics or r["window_id"] not in windows:raise ObservationError("unknown metric/window")
  key=(r["cell_id"],r["metric_id"],r["window_id"])
  if key in seen:raise ObservationError("duplicate observation")
  if r["known_time"]>cutoff or r["known_time"]>windows[r["window_id"]]["end_known_time"] or r["future_suffix_used"] is not False:raise ObservationError("future-suffix evidence")
  if r["synthetic_fixture"] is not True:raise ObservationError("reference observations must be synthetic")
  integer(r["sample_count"],"sample_count",1);number(r["value"],"value");number(r["baseline_value"],"baseline_value")
  if r["sample_count"]<metrics[r["metric_id"]]["minimum_samples"]:raise ObservationError("insufficient samples")
  out.append(deepcopy(r));seen.add(key)
 expected=len(cells)*len(metrics)*len(windows);coverage_bps=int(len(out)*10000/expected)
 if coverage_bps<policy["minimum_metric_coverage_bps"]:raise ObservationError("coverage below policy")
 ordered=sorted(out,key=lambda z:(z["known_time"],z["cell_id"],z["metric_id"],z["window_id"]))
 chain=hash_chain(ordered,"v441_observation")
 return seal({"phase":"SAED_V4_41","registry_hash":registry["compiled_registry_hash"],"policy_hash":policy["frozen_policy_hash"],"cutoff":cutoff,"rows":chain,"observation_count":len(chain),"expected_count":expected,"coverage_bps":coverage_bps,"coverage_complete":len(chain)==expected,"future_suffix_used":False,"immutable":True,"research_only":True},"v441_observation_ledger","ledger_id","ledger_hash")
