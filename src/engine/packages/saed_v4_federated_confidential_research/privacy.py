from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_nonnegative
from .errors import PrivacyError
from .canonical import content_hash,seal,hash_chain

def freeze_privacy(policy:dict)->dict:
    require_exact(policy,["policy_id","mechanism","total_epsilon","delta","per_round_epsilon","clip_norm","max_rounds","accountant","synthetic_noise_seed","formal_privacy_guarantee_claimed","research_only"])
    for k in ["total_epsilon","delta","per_round_epsilon","clip_norm"]: require_nonnegative(policy[k],k)
    if policy["total_epsilon"]<=0 or policy["per_round_epsilon"]<=0 or policy["clip_norm"]<=0: raise PrivacyError("privacy parameters must be positive")
    if policy["formal_privacy_guarantee_claimed"] or policy["research_only"] is not True: raise PrivacyError("formal privacy guarantee not allowed")
    if policy["per_round_epsilon"]*policy["max_rounds"]>policy["total_epsilon"]+1e-12: raise PrivacyError("privacy budget overcommitted")
    body=deepcopy(policy); body["policy_hash"]=content_hash(body); return body

def clip(vector:list[float],limit:float)->tuple[list[float],float,bool]:
    norm=sum(float(x)*float(x) for x in vector)**0.5
    if norm<=limit or norm==0: return [round(float(x),12) for x in vector],round(norm,12),False
    scale=limit/norm
    return [round(float(x)*scale,12) for x in vector],round(norm,12),True

def budget_ledger(policy:dict,rounds:list[dict])->dict:
    events=[]; spent=0.0
    for r in rounds:
        eps=policy["per_round_epsilon"] if r["released"] else 0.0; spent=round(spent+eps,12)
        if spent>policy["total_epsilon"]+1e-12: raise PrivacyError("privacy budget exhausted")
        events.append({"round_id":r["round_id"],"epsilon_spent":eps,"cumulative_epsilon":spent,"delta":policy["delta"],"released":r["released"]})
    chained=hash_chain(events,"v433_privacy_event")
    return seal({"phase":"SAED_V4_33","policy_id":policy["policy_id"],"events":chained,"total_epsilon":policy["total_epsilon"],"spent_epsilon":spent,"remaining_epsilon":round(policy["total_epsilon"]-spent,12),"budget_respected":spent<=policy["total_epsilon"],"formal_dp_guarantee":"not_claimed","research_only":True},"v433_privacy_budget","ledger_id","ledger_hash")
