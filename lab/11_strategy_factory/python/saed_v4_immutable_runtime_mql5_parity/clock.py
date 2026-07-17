from __future__ import annotations
from copy import deepcopy
from .contracts import exact,enum,integer,sorted_unique_strings
from .errors import ClockProfileError
from .canonical import seal

def freeze_clock_profile(v:dict)->dict:
 exact(v,["clock_profile_id","timezone","timestamp_format","bar_close_only","session_calendar_id","allowed_weekdays","dst_policy","missing_bar_policy","duplicate_timestamp_policy","out_of_order_policy","max_clock_skew_ms","research_only"])
 if v["timezone"]!="UTC" or v["timestamp_format"]!="RFC3339_NANO_UTC":raise ClockProfileError("UTC RFC3339 required")
 if v["bar_close_only"] is not True or v["research_only"] is not True:raise ClockProfileError("clock authority invalid")
 sorted_unique_strings(v["allowed_weekdays"],"allowed_weekdays",5)
 enum(v["dst_policy"],{"UTC_ONLY"},"dst_policy"); enum(v["missing_bar_policy"],{"ABSTAIN"},"missing_bar_policy"); enum(v["duplicate_timestamp_policy"],{"REJECT"},"duplicate_timestamp_policy"); enum(v["out_of_order_policy"],{"REJECT"},"out_of_order_policy")
 integer(v["max_clock_skew_ms"],"max_clock_skew_ms",0,5000)
 return seal(deepcopy(v),"v438_clock","frozen_clock_id","clock_hash")

def validate_timestamps(rows:list[dict],cutoff:str)->dict:
 seen=set(); prev=""
 for r in rows:
  t=r["known_time"]
  if t>cutoff:raise ClockProfileError("future known_time")
  if t in seen:raise ClockProfileError("duplicate timestamp")
  if prev and t<prev:raise ClockProfileError("out of order timestamp")
  seen.add(t); prev=t
 return {"row_count":len(rows),"first_time":rows[0]["known_time"] if rows else "","last_time":rows[-1]["known_time"] if rows else "","passed":True}
