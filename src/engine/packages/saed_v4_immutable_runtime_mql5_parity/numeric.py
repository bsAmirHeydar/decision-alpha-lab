from __future__ import annotations
from copy import deepcopy
from .contracts import exact,enum,number,integer
from .errors import NumericProfileError
from .canonical import seal,q,dec
ROUNDING={"HALF_EVEN"}; NAN={"REJECT"}; INF={"REJECT"}

def freeze_numeric_profile(v:dict)->dict:
 exact(v,["profile_id","float_mode","rounding_mode","decimal_places","absolute_tolerance","relative_tolerance","nan_policy","infinity_policy","division_zero_policy","comparison_epsilon","research_only"])
 if v["float_mode"]!="IEEE754_BINARY64":raise NumericProfileError("binary64 required")
 enum(v["rounding_mode"],ROUNDING,"rounding_mode"); integer(v["decimal_places"],"decimal_places",6,12)
 number(v["absolute_tolerance"],"absolute_tolerance",0,1e-5); number(v["relative_tolerance"],"relative_tolerance",0,1e-5); number(v["comparison_epsilon"],"comparison_epsilon",0,1e-5)
 enum(v["nan_policy"],NAN,"nan_policy"); enum(v["infinity_policy"],INF,"infinity_policy")
 if v["division_zero_policy"]!="ABSTAIN":raise NumericProfileError("division by zero must abstain")
 if v["research_only"] is not True:raise NumericProfileError("research_only required")
 return seal(deepcopy(v),"v438_numeric","frozen_profile_id","profile_hash")
def quantize(x:float,places:int=8)->float:
 scale=dec(10)**places; return float((dec(x)*scale).to_integral_value(rounding="ROUND_HALF_EVEN")/scale)
def close(a:float,b:float,p:dict)->bool:
 d=abs(float(a)-float(b)); return d<=max(float(p["absolute_tolerance"]),float(p["relative_tolerance"])*max(abs(float(a)),abs(float(b))))
