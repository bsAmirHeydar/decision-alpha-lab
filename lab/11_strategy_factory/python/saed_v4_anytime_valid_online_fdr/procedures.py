from __future__ import annotations
from dataclasses import dataclass
from .sequences import gamma_at
from .errors import ProcedureError

@dataclass
class Decision:
    local_index:int; alpha:float; rejected:bool; wealth_before:float; reward:float; wealth_after:float; candidate:bool; discarded:bool

def _reject(record,alpha,procedure):
    if procedure=="e_lond": return record["e_value"]>=(1.0/max(alpha,1e-18))
    return record["anytime_p_value"]<=alpha

def run_family(procedure,records,q,weights,policy):
    if q<=0: return []
    wealth=q*policy.initial_wealth_fraction; reward_unit=q*policy.reward_fraction; cap=q*policy.maximum_alpha_fraction
    rejections=[]; candidate_count=0; selected_count=0; out=[]
    for k,r in enumerate(records,1):
        p=r["anytime_p_value"]; candidate=p<=policy.candidate_threshold; discarded=p>policy.discard_threshold
        candidate_count+=int(candidate); selected_count+=int(not discarded)
        if procedure=="alpha_spending": proposed=q*gamma_at(weights,k)
        elif procedure=="alpha_investing": proposed=wealth*policy.maximum_spend_fraction
        elif procedure=="lord_plus_plus":
            proposed=q*policy.initial_wealth_fraction*gamma_at(weights,k)
            for j,tau in enumerate(rejections): proposed+=(q*(1-policy.initial_wealth_fraction) if j==0 else q)*gamma_at(weights,k-tau)
        elif procedure=="saffron":
            idx=max(1,candidate_count+1); proposed=(1-policy.candidate_threshold)*q*gamma_at(weights,idx)*(1+len(rejections))
        elif procedure=="addis":
            if discarded: proposed=0.0
            else: proposed=(policy.discard_threshold-policy.candidate_threshold)*q*gamma_at(weights,max(1,selected_count))*(1+len(rejections))
        elif procedure=="e_lond": proposed=q*gamma_at(weights,k)*(1+len(rejections))
        else: raise ProcedureError("unknown procedure")
        alpha=max(0.0,min(cap,proposed,wealth*policy.maximum_spend_fraction if procedure!="alpha_spending" else wealth))
        rejected=bool(r["eligible"] and _reject(r,alpha,procedure)); reward=reward_unit if rejected else 0.0
        after=wealth-alpha+reward
        if after<-1e-15: raise ProcedureError("negative wealth")
        after=max(0.0,after)
        if rejected: rejections.append(k)
        out.append(Decision(k,alpha,rejected,wealth,reward,after,candidate,discarded)); wealth=after
    return out

def run_all(records_by_family,allocations,weights,policy,procedures):
    result={}
    for procedure in procedures:
        fam={}
        for a in allocations:
            fid=a["family_id"]; q=policy.target_fdr*a["weight"]; recs=records_by_family.get(fid,[])
            fam[fid]=run_family(procedure,recs,q,weights,policy)
        result[procedure]=fam
    return result
