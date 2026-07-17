from __future__ import annotations
from .canonical import seal,q
from .contracts import require_list,require_exact,require_unique,require_num
from .errors import ReconciliationError

def reconcile(schedule:dict,synthetic_fills:list[dict],economics:dict)->dict:
    fills=require_list(synthetic_fills,"synthetic_fills",1); require_unique(fills,"fill_id","synthetic_fills"); fills=sorted(fills,key=lambda x:x["fill_id"]); scheduled={o["opportunity_id"]:o for o in schedule["orders"]}; emap={x["opportunity_id"]:x for x in economics["rows"]}; rows=[]
    for f in fills:
        require_exact(f,["fill_id","opportunity_id","filled_units","realized_cost_bps","realized_slippage_bps","synthetic_fixture"])
        require_num(f["filled_units"],"filled_units",0); require_num(f["realized_cost_bps"],"realized_cost_bps",0); require_num(f["realized_slippage_bps"],"realized_slippage_bps",0)
        if f["opportunity_id"] not in scheduled: raise ReconciliationError("fill without schedule")
        planned=scheduled[f["opportunity_id"]]["total_units"]; expected=float(emap[f["opportunity_id"]]["expected_total_cost_bps"]); realized=float(f["realized_cost_bps"])+float(f["realized_slippage_bps"])
        rows.append({"fill_id":f["fill_id"],"opportunity_id":f["opportunity_id"],"planned_units":planned,"filled_units":float(f["filled_units"]),"fill_ratio":float(q(float(f["filled_units"])/planned if planned else 0)),"expected_cost_bps":float(q(expected)),"realized_cost_bps":float(q(realized)),"cost_variance_bps":float(q(realized-expected)),"synthetic_only":True})
    return seal({"phase":"SAED_V4_37","rows":rows,"all_synthetic":True,"broker_evidence_present":False,"research_only":True},"v437_reconciliation","report_id","report_hash")
