from __future__ import annotations
from collections import Counter
from .canonical import seal,content_hash
def build_surveillance_dashboard(registry:dict,policy:dict,ledger:dict,detection:dict,fusion:dict,incidents:dict,retirement:dict)->dict:
 tenant_actions={}
 for t in sorted(registry["tenants"]):tenant_actions[t]=dict(Counter(x["action"] for x in fusion["rows"] if x["tenant_id"]==t))
 return seal({"phase":"SAED_V4_41","fleet_cell_count":len(registry["cells"]),"metric_count":len(policy["metrics"]),"window_count":len(policy["windows"]),"observation_count":ledger["observation_count"],"coverage_bps":ledger["coverage_bps"],"alert_count":detection["alert_count"],"action_counts":fusion["action_counts"],"incident_count":incidents["incident_count"],"retirement_candidate_count":retirement["candidate_count"],"retired_count":retirement["retired_count"],"pending_retirement_count":retirement["pending_count"],"tenant_actions":tenant_actions,"future_suffix_used":False,"live_order_side_effects":0,"capital_delta":0.0,"unknown_cells":0,"research_only":True},"v441_dashboard","dashboard_id","dashboard_hash")
