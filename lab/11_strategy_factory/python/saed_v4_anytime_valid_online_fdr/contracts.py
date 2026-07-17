from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping
from .errors import ContractError

PROCEDURES=("alpha_spending","alpha_investing","lord_plus_plus","saffron","addis","e_lond")
EVIDENCE_TYPES=("anytime_p","e_process","dual")
DATA_ROLES=("public","synthetic","train","validation","stress","negative")
TRUTH_LABELS=("null","alternative")
INVALID_ACTIONS=("skip","quarantine")

def exact(v:Mapping[str,Any],required:set[str],label:str):
    if not isinstance(v,Mapping): raise ContractError(f"{label} must be object")
    if set(v)!=required: raise ContractError(f"{label} field mismatch: unknown={sorted(set(v)-required)}, missing={sorted(required-set(v))}")
def text(v:Any,label:str)->str:
    x=str(v).strip()
    if not x: raise ContractError(f"{label} empty")
    return x
def number(v:Any,label:str,minimum:float|None=None,maximum:float|None=None)->float:
    try: x=float(v)
    except Exception as exc: raise ContractError(f"{label} not numeric") from exc
    if not (x==x and abs(x)!=float("inf")): raise ContractError(f"{label} non-finite")
    if minimum is not None and x<minimum: raise ContractError(f"{label} below {minimum}")
    if maximum is not None and x>maximum: raise ContractError(f"{label} above {maximum}")
    return x
def integer(v:Any,label:str,minimum:int=0)->int:
    if isinstance(v,bool): raise ContractError(f"{label} boolean")
    try: x=int(v)
    except Exception as exc: raise ContractError(f"{label} not integer") from exc
    if x<minimum: raise ContractError(f"{label} below {minimum}")
    return x
def true(v:Any,label:str)->bool:
    if v is not True: raise ContractError(f"{label} must be true")
    return True
def timestamp(v:Any,label:str)->str:
    x=text(v,label)
    try: datetime.fromisoformat(x.replace("Z","+00:00"))
    except Exception as exc: raise ContractError(f"{label} invalid ISO timestamp") from exc
    return x

@dataclass(frozen=True)
class UpstreamIntake:
    required_phase:str; exact_version:str; certificate_hash:str; handoff_hash:str; multiplicity_universe_hash:str; immutable:bool; hash_verified:bool; research_only:bool
    @classmethod
    def parse(cls,v):
        req={"required_phase","exact_version","certificate_hash","handoff_hash","multiplicity_universe_hash","immutable","hash_verified","research_only"}; exact(v,req,"upstream_intake")
        out=cls(text(v["required_phase"],"required_phase"),text(v["exact_version"],"exact_version"),text(v["certificate_hash"],"certificate_hash"),text(v["handoff_hash"],"handoff_hash"),text(v["multiplicity_universe_hash"],"multiplicity_universe_hash"),bool(v["immutable"]),bool(v["hash_verified"]),bool(v["research_only"]))
        if out.required_phase!="SAED_V4_27" or out.exact_version!="1.0.0": raise ContractError("V4-28 requires exact V4-27 v1.0.0")
        if not (out.immutable and out.hash_verified and out.research_only): raise ContractError("unsafe upstream intake")
        return out

@dataclass(frozen=True)
class FDRPolicy:
    exact_version:str; target_fdr:float; primary_procedure:str; initial_wealth_fraction:float; reward_fraction:float; maximum_alpha_fraction:float; maximum_spend_fraction:float; candidate_threshold:float; discard_threshold:float; anytime_valid_required:bool; predictable_allocation_required:bool; family_scoped:bool; nonnegative_wealth_required:bool; no_retroactive_mutation:bool; rejection_requires_crossing:bool; deterministic:bool; research_only:bool; invalid_evidence_action:str
    @classmethod
    def parse(cls,v):
        req={"exact_version","target_fdr","primary_procedure","initial_wealth_fraction","reward_fraction","maximum_alpha_fraction","maximum_spend_fraction","candidate_threshold","discard_threshold","anytime_valid_required","predictable_allocation_required","family_scoped","nonnegative_wealth_required","no_retroactive_mutation","rejection_requires_crossing","deterministic","research_only","invalid_evidence_action"}; exact(v,req,"fdr_policy")
        out=cls(text(v["exact_version"],"exact_version"),number(v["target_fdr"],"target_fdr",1e-9,0.25),text(v["primary_procedure"],"primary_procedure"),number(v["initial_wealth_fraction"],"initial_wealth_fraction",1e-9,1.0),number(v["reward_fraction"],"reward_fraction",0.0,1.0),number(v["maximum_alpha_fraction"],"maximum_alpha_fraction",1e-9,1.0),number(v["maximum_spend_fraction"],"maximum_spend_fraction",1e-9,1.0),number(v["candidate_threshold"],"candidate_threshold",1e-9,1.0),number(v["discard_threshold"],"discard_threshold",1e-9,1.0),*[bool(v[k]) for k in ["anytime_valid_required","predictable_allocation_required","family_scoped","nonnegative_wealth_required","no_retroactive_mutation","rejection_requires_crossing","deterministic","research_only"]],text(v["invalid_evidence_action"],"invalid_evidence_action"))
        if out.primary_procedure not in PROCEDURES: raise ContractError("unknown primary procedure")
        if out.invalid_evidence_action not in INVALID_ACTIONS: raise ContractError("unknown invalid evidence action")
        if not all(getattr(out,k) for k in ["anytime_valid_required","predictable_allocation_required","family_scoped","nonnegative_wealth_required","no_retroactive_mutation","rejection_requires_crossing","deterministic","research_only"]): raise ContractError("FDR policy must fail closed")
        if out.candidate_threshold>=out.discard_threshold: raise ContractError("candidate_threshold must be below discard_threshold")
        return out

@dataclass(frozen=True)
class GammaPolicy:
    exact_version:str; weights:tuple[float,...]; normalized:bool; nonincreasing:bool; deterministic:bool
    @classmethod
    def parse(cls,v):
        req={"exact_version","weights","normalized","nonincreasing","deterministic"}; exact(v,req,"gamma_policy")
        weights=tuple(number(x,"gamma_weight",0.0,1.0) for x in v["weights"])
        out=cls(text(v["exact_version"],"exact_version"),weights,bool(v["normalized"]),bool(v["nonincreasing"]),bool(v["deterministic"]))
        if len(weights)<64: raise ContractError("gamma sequence too short")
        if not (out.normalized and out.nonincreasing and out.deterministic): raise ContractError("gamma policy must be deterministic, normalized and nonincreasing")
        if abs(sum(weights)-1.0)>1e-12: raise ContractError("gamma weights must sum to one")
        if any(weights[i+1]>weights[i]+1e-15 for i in range(len(weights)-1)): raise ContractError("gamma weights not nonincreasing")
        return out

def parse_family_allocation(items):
    req={"family_id","weight","frozen_before_first_test","owner_actor_id","allocation_basis","maximum_hypotheses"}; out=[]; seen=set()
    for v in items:
        exact(v,req,"family_allocation")
        fid=text(v["family_id"],"family_id")
        if fid in seen: raise ContractError("duplicate family allocation")
        if v["frozen_before_first_test"] is not True: raise ContractError("family allocation not frozen")
        out.append({**dict(v),"weight":number(v["weight"],"weight",0.0,1.0),"maximum_hypotheses":integer(v["maximum_hypotheses"],"maximum_hypotheses",1)}); seen.add(fid)
    if not out or abs(sum(x["weight"] for x in out)-1.0)>1e-12: raise ContractError("family weights must sum to one")
    return sorted(out,key=lambda x:x["family_id"])

def parse_stopping_rules(items):
    req={"stopping_rule_id","name","rule_type","predictable","uses_future_data","maximum_looks","description"}; out=[]; seen=set()
    for v in items:
        exact(v,req,"stopping_rule")
        rid=text(v["stopping_rule_id"],"stopping_rule_id")
        if rid in seen: raise ContractError("duplicate stopping rule")
        if v["predictable"] is not True or v["uses_future_data"] is not False: raise ContractError("unsafe stopping rule")
        x=dict(v); x["maximum_looks"]=integer(v["maximum_looks"],"maximum_looks",1); out.append(x); seen.add(rid)
    if not out: raise ContractError("empty stopping rule registry")
    return sorted(out,key=lambda x:x["stopping_rule_id"])

def parse_challengers(items):
    req={"procedure","enabled","role","promotion_authority","notes"}; out=[]; seen=set()
    for v in items:
        exact(v,req,"challenger")
        p=text(v["procedure"],"procedure")
        if p not in PROCEDURES or p in seen: raise ContractError("invalid challenger procedure")
        if v["promotion_authority"] is not False: raise ContractError("challenger authority escape")
        out.append(dict(v)); seen.add(p)
    if seen!=set(PROCEDURES): raise ContractError("challenger registry incomplete")
    return sorted(out,key=lambda x:x["procedure"])

def parse_hypotheses(items,family_ids:set[str],stopping_ids:set[str]):
    hreq={"hypothesis_id","sequence","family_id","experiment_id","trial_id","metric_name","direction","null_boundary","decision_time","stopping_rule_id","actor_id","data_role","manifest_hash","truth_label","synthetic_fixture","eligible","looks"}
    lreq={"look_sequence","known_at","anytime_p_value","e_value","statistic","evidence_hash"}
    out=[]; seen=set(); seqs=[]
    for v in items:
        exact(v,hreq,"hypothesis")
        hid=text(v["hypothesis_id"],"hypothesis_id")
        if hid in seen: raise ContractError("duplicate hypothesis_id")
        seq=integer(v["sequence"],"sequence",1); seqs.append(seq)
        if v["family_id"] not in family_ids: raise ContractError("unknown family_id")
        if v["stopping_rule_id"] not in stopping_ids: raise ContractError("unknown stopping_rule_id")
        if v["data_role"] not in DATA_ROLES: raise ContractError("forbidden data role")
        if v["truth_label"] not in TRUTH_LABELS or v["synthetic_fixture"] is not True: raise ContractError("reference hypotheses require synthetic truth")
        decision=timestamp(v["decision_time"],"decision_time")
        looks=[]; lseq=[]
        for look in v["looks"]:
            exact(look,lreq,"look")
            ls=integer(look["look_sequence"],"look_sequence",1); lseq.append(ls)
            looks.append({**dict(look),"look_sequence":ls,"known_at":timestamp(look["known_at"],"known_at"),"anytime_p_value":number(look["anytime_p_value"],"anytime_p_value",0.0,1.0),"e_value":number(look["e_value"],"e_value",0.0,None),"statistic":number(look["statistic"],"statistic")})
        if lseq!=list(range(1,len(lseq)+1)) or not looks: raise ContractError("look sequence must be contiguous")
        p=[x["anytime_p_value"] for x in looks]
        if any(p[i+1]>p[i]+1e-15 for i in range(len(p)-1)): raise ContractError("reported anytime p process must be running-min nonincreasing")
        x=dict(v); x["sequence"]=seq; x["decision_time"]=decision; x["looks"]=looks; out.append(x); seen.add(hid)
    if seqs!=list(range(1,len(seqs)+1)): raise ContractError("hypothesis sequence must be contiguous and ordered")
    return out

def parse_config(config):
    req={"upstream_intake","fdr_policy","gamma_policy","family_allocation","stopping_rule_registry","challenger_registry"}; exact(config,req,"full_config")
    fam=parse_family_allocation(config["family_allocation"]); stops=parse_stopping_rules(config["stopping_rule_registry"])
    return {"upstream_intake":UpstreamIntake.parse(config["upstream_intake"]),"fdr_policy":FDRPolicy.parse(config["fdr_policy"]),"gamma_policy":GammaPolicy.parse(config["gamma_policy"]),"family_allocation":fam,"stopping_rule_registry":stops,"challenger_registry":parse_challengers(config["challenger_registry"])}
