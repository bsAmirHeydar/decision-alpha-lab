from __future__ import annotations
from copy import deepcopy
from .canonical import seal
from .contracts import require_exact,require_num,require_int
from .errors import BudgetError

def freeze_budgets(v:dict)->dict:
    require_exact(v,["budget_id","compute_units","exposure_units","review_hours","max_candidates","max_selected","max_parallel","risk_capacity","reserve_fraction","approved_by","research_only"])
    for k in ["compute_units","exposure_units","review_hours","risk_capacity"]: require_num(v[k],k,0)
    for k in ["max_candidates","max_selected","max_parallel"]: require_int(v[k],k,1)
    require_num(v["reserve_fraction"],"reserve_fraction",0,0.9)
    if v["max_selected"]>v["max_candidates"] or v["research_only"] is not True: raise BudgetError("budget invalid")
    return seal(deepcopy(v)|{"phase":"SAED_V4_36","automatic_overrun_allowed":False},"v436_budget","budget_receipt_id","budget_hash")

def available(budget:dict)->dict:
    r=budget["reserve_fraction"]
    return seal({"phase":"SAED_V4_36","compute_units":round(budget["compute_units"]*(1-r),8),"exposure_units":round(budget["exposure_units"]*(1-r),8),"review_hours":round(budget["review_hours"]*(1-r),8),"risk_capacity":round(budget["risk_capacity"]*(1-r),8),"max_selected":budget["max_selected"],"max_parallel":budget["max_parallel"],"reserve_fraction":r,"research_only":True},"v436_available","availability_id","availability_hash")
