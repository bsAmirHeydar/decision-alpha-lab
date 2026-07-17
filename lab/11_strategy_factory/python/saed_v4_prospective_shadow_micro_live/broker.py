from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,number,integer,sorted_unique_strings
from .errors import BrokerError
from .canonical import content_hash,seal

def freeze_broker_profile(v:dict)->dict:
 exact(v,["broker_profile_id","version","environment","server","account_currency","account_type","symbols","capabilities","sessions","rate_limits","demo_only","credentials_embedded","research_only"])
 if v["environment"]!="SYNTHETIC_DEMO_REFERENCE" or v["demo_only"] is not True or v["credentials_embedded"] is not False or v["research_only"] is not True:raise BrokerError("broker profile boundary invalid")
 syms=list_of(v["symbols"],"symbols",1);unique(syms,"symbol","symbols")
 for s in syms:
  exact(s,["symbol","digits","point","tick_size","tick_value","min_volume","max_volume","volume_step","stop_level_points","freeze_level_points","max_spread_bps"])
  integer(s["digits"],"digits",0,10)
  for k in ["point","tick_size","tick_value","min_volume","max_volume","volume_step","max_spread_bps"]:number(s[k],k,0)
  integer(s["stop_level_points"],"stop_level_points",0);integer(s["freeze_level_points"],"freeze_level_points",0)
 caps=sorted_unique_strings(v["capabilities"],"capabilities",4)
 required={"MARKET_DATA","PAPER_LEDGER","SHADOW_DECISIONS","POSITION_SNAPSHOT"}
 if not required<=set(caps):raise BrokerError("required capabilities missing")
 x=deepcopy(v);x["symbols"]=sorted(syms,key=lambda z:z["symbol"]);x["broker_profile_hash"]=content_hash(x);return seal(x,"v439_broker","frozen_broker_id","frozen_broker_hash")

def qualification_matrix(profile:dict,evidence_items:list[dict])->dict:
 types={x["evidence_type"]:x for x in evidence_items}
 checks=[]
 for gate in ["SYMBOL_METADATA","SESSION_CALENDAR","SPREAD_CAPTURE","LATENCY_CAPTURE","REJECT_CAPTURE","POSITION_SNAPSHOT","DEMO_CONNECTIVITY","LIVE_CONNECTIVITY"]:
  item=types.get(gate);passed=bool(item and item["status"]=="PASSED" and item["actual_external_evidence"] is True)
  checks.append({"gate_id":gate,"passed":passed,"status":item["status"] if item else "MISSING","actual_external_evidence":bool(item and item["actual_external_evidence"] is True)})
 return seal({"phase":"SAED_V4_39","broker_profile_hash":profile["frozen_broker_hash"],"checks":checks,"demo_qualified":all(x["passed"] for x in checks if x["gate_id"]!="LIVE_CONNECTIVITY"),"live_qualified":all(x["passed"] for x in checks),"research_only":True,"production_authorized":False},"v439_broker_matrix","matrix_id","matrix_hash")
