from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .errors import ContractError

TRIAL_STATES=("proposed","compiled","duplicate","invalid","running","pruned","failed","timed_out","cancelled","completed","selected","rejected")
TERMINAL_STATES={"duplicate","invalid","pruned","failed","timed_out","cancelled","selected","rejected"}
DATA_ROLES=("public","synthetic","train","validation","stress","negative","hidden_evaluation","protected_final")
EXPOSURE_TYPES=("dashboard_open","chart_render","metric_read","example_inspection","agent_summary","row_export","narrative_generated","hypothesis_modified","manual_intervention","notebook_open","query_submitted")
ACTOR_TYPES=("human","agent","service","validator")
SEARCH_MODES=("grid","random","quasi_random","bayesian","hyperband","evolutionary","manual","diagnostic")


def exact(v: Mapping[str,Any], required:set[str], label:str):
    if set(v)!=required:
        raise ContractError(f"{label} field mismatch: unknown={sorted(set(v)-required)}, missing={sorted(required-set(v))}")
def text(v:Any,label:str)->str:
    x=str(v).strip()
    if not x: raise ContractError(f"{label} empty")
    return x
def integer(v:Any,label:str,minimum:int=0)->int:
    x=int(v)
    if x<minimum: raise ContractError(f"{label} below {minimum}")
    return x

def boolean_true(v:Any,label:str)->bool:
    if v is not True: raise ContractError(f"{label} must be true")
    return True

@dataclass(frozen=True)
class UpstreamIntake:
    required_phase:str; exact_version:str; certificate_hash:str; handoff_hash:str; immutable:bool; hash_verified:bool; research_only:bool
    @classmethod
    def parse(cls,v):
        req={"required_phase","exact_version","certificate_hash","handoff_hash","immutable","hash_verified","research_only"}; exact(v,req,"upstream_intake")
        out=cls(text(v["required_phase"],"required_phase"),text(v["exact_version"],"exact_version"),text(v["certificate_hash"],"certificate_hash"),text(v["handoff_hash"],"handoff_hash"),bool(v["immutable"]),bool(v["hash_verified"]),bool(v["research_only"]))
        if out.required_phase!="SAED_V4_26": raise ContractError("V4-27 requires exact V4-26")
        if not (out.immutable and out.hash_verified and out.research_only): raise ContractError("unsafe upstream intake")
        return out

@dataclass(frozen=True)
class LedgerPolicy:
    exact_version:str; append_only:bool; hash_chain_required:bool; actor_identity_required:bool; data_role_required:bool; known_time_required:bool; complete_failure_accounting:bool; duplicate_accounting:bool; retry_accounting:bool; orphan_runs_forbidden:bool; protected_exposure_forbidden:bool; hidden_evaluation_query_budget:int; deterministic:bool
    @classmethod
    def parse(cls,v):
        req={"exact_version","append_only","hash_chain_required","actor_identity_required","data_role_required","known_time_required","complete_failure_accounting","duplicate_accounting","retry_accounting","orphan_runs_forbidden","protected_exposure_forbidden","hidden_evaluation_query_budget","deterministic"}; exact(v,req,"ledger_policy")
        out=cls(text(v["exact_version"],"exact_version"),*[bool(v[k]) for k in ["append_only","hash_chain_required","actor_identity_required","data_role_required","known_time_required","complete_failure_accounting","duplicate_accounting","retry_accounting","orphan_runs_forbidden","protected_exposure_forbidden"]],integer(v["hidden_evaluation_query_budget"],"hidden_evaluation_query_budget"),bool(v["deterministic"]))
        if not all(getattr(out,k) for k in ["append_only","hash_chain_required","actor_identity_required","data_role_required","known_time_required","complete_failure_accounting","duplicate_accounting","retry_accounting","orphan_runs_forbidden","protected_exposure_forbidden","deterministic"]): raise ContractError("ledger policy must fail closed")
        if out.hidden_evaluation_query_budget!=0: raise ContractError("V4-27 hidden evaluation budget must remain zero")
        return out

@dataclass(frozen=True)
class QueryBudget:
    exact_version:str; maximum_trials:int; maximum_exposures:int; maximum_chart_renders:int; maximum_metric_reads:int; maximum_agent_summaries:int; maximum_row_exports:int; maximum_narratives:int; maximum_hypothesis_modifications:int; maximum_manual_interventions:int; maximum_hidden_evaluation_queries:int; maximum_protected_exposures:int; maximum_runtime_compilations:int; maximum_order_submissions:int; maximum_online_mutations:int
    @classmethod
    def parse(cls,v):
        names=["maximum_trials","maximum_exposures","maximum_chart_renders","maximum_metric_reads","maximum_agent_summaries","maximum_row_exports","maximum_narratives","maximum_hypothesis_modifications","maximum_manual_interventions","maximum_hidden_evaluation_queries","maximum_protected_exposures","maximum_runtime_compilations","maximum_order_submissions","maximum_online_mutations"]
        exact(v,{"exact_version",*names},"query_budget")
        out=cls(text(v["exact_version"],"exact_version"),*[integer(v[k],k) for k in names])
        for k in ["maximum_hidden_evaluation_queries","maximum_protected_exposures","maximum_runtime_compilations","maximum_order_submissions","maximum_online_mutations"]:
            if getattr(out,k)!=0: raise ContractError(f"{k} must remain zero")
        return out

def parse_actor_registry(items):
    req={"actor_id","actor_type","display_name","organization","role","active","credential_scope","created_at"}
    ids=set(); out=[]
    for v in items:
        exact(v,req,"actor")
        if v["actor_type"] not in ACTOR_TYPES: raise ContractError("unknown actor_type")
        if not v["active"]: raise ContractError("inactive actor in frozen registry")
        if v["actor_id"] in ids: raise ContractError("duplicate actor_id")
        ids.add(v["actor_id"]); out.append(dict(v))
    if not out: raise ContractError("empty actor registry")
    return out

def parse_data_roles(items):
    req={"data_role","protected","allowed_exposure_types","query_budget","description"}
    roles=set(); out=[]
    for v in items:
        exact(v,req,"data_role")
        if v["data_role"] not in DATA_ROLES: raise ContractError("unknown data role")
        if v["data_role"] in roles: raise ContractError("duplicate data role")
        if not set(v["allowed_exposure_types"]).issubset(EXPOSURE_TYPES): raise ContractError("unknown exposure type")
        if v["data_role"] in {"hidden_evaluation","protected_final"} and int(v["query_budget"])!=0: raise ContractError("protected role budget nonzero")
        roles.add(v["data_role"]); out.append(dict(v))
    if roles!=set(DATA_ROLES): raise ContractError("incomplete data role registry")
    return out

def parse_search_families(items):
    req={"family_id","name","mode","hypothesis_family","parameter_space_hash","frozen_before_search","owner_actor_id","maximum_trials","selection_metric","data_roles_allowed"}
    ids=set(); out=[]
    for v in items:
        exact(v,req,"search_family")
        if v["mode"] not in SEARCH_MODES: raise ContractError("unknown search mode")
        if not v["frozen_before_search"]: raise ContractError("search family not frozen")
        if v["family_id"] in ids: raise ContractError("duplicate family_id")
        if not set(v["data_roles_allowed"]).issubset(set(DATA_ROLES)-{"hidden_evaluation","protected_final"}): raise ContractError("protected role admitted to search")
        ids.add(v["family_id"]); out.append(dict(v))
    if not out: raise ContractError("empty search families")
    return out

def parse_manifests(items):
    req={"experiment_id","family_id","manifest_hash","code_hash","config_hash","dataset_hash","data_role","owner_actor_id","created_at","expected_trial_ids","budget_trials","parent_experiment_id","research_only"}
    ids=set(); trials=set(); out=[]
    for v in items:
        exact(v,req,"experiment_manifest")
        if v["data_role"] in {"hidden_evaluation","protected_final"}: raise ContractError("protected experiment forbidden")
        if not v["research_only"]: raise ContractError("manifest authority escape")
        if v["experiment_id"] in ids: raise ContractError("duplicate experiment_id")
        ids.add(v["experiment_id"])
        for tid in v["expected_trial_ids"]:
            if tid in trials: raise ContractError("trial claimed by multiple manifests")
            trials.add(tid)
        if len(v["expected_trial_ids"])>int(v["budget_trials"]): raise ContractError("manifest exceeds budget")
        out.append(dict(v))
    return out

def parse_config(config):
    req={"upstream_intake","ledger_policy","query_budget","actor_registry","data_role_registry","search_family_registry"}; exact(config,req,"full_config")
    return {"upstream_intake":UpstreamIntake.parse(config["upstream_intake"]),"ledger_policy":LedgerPolicy.parse(config["ledger_policy"]),"query_budget":QueryBudget.parse(config["query_budget"]),"actor_registry":parse_actor_registry(config["actor_registry"]),"data_role_registry":parse_data_roles(config["data_role_registry"]),"search_family_registry":parse_search_families(config["search_family_registry"])}
