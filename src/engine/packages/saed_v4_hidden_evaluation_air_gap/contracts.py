from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any,Mapping
from .errors import ContractError

ALLOWED_TRAINING_ROLES=("public","train","validation","stress","synthetic","negative")
FORBIDDEN_DISCLOSURE_FIELDS={"record_id","hidden_label","prediction","probability","row","rows","confusion_matrix","raw_score","feature_vector","key_share","plaintext"}
METRICS=("balanced_accuracy","accuracy","brier_score","log_loss","roc_auc","delta_balanced_accuracy_vs_baseline")

def exact(v:Mapping[str,Any],required:set[str],label:str):
    if not isinstance(v,Mapping): raise ContractError(f"{label} must be object")
    unknown=set(v)-required; missing=required-set(v)
    if unknown or missing: raise ContractError(f"{label} field mismatch: unknown={sorted(unknown)}, missing={sorted(missing)}")
def text(v:Any,label:str)->str:
    x=str(v).strip()
    if not x: raise ContractError(f"{label} empty")
    return x
def boolean(v:Any,label:str,expected:bool|None=None)->bool:
    if not isinstance(v,bool): raise ContractError(f"{label} must be boolean")
    if expected is not None and v is not expected: raise ContractError(f"{label} must be {expected}")
    return v
def integer(v:Any,label:str,minimum:int=0,maximum:int|None=None)->int:
    if isinstance(v,bool): raise ContractError(f"{label} boolean")
    try: x=int(v)
    except Exception as exc: raise ContractError(f"{label} not integer") from exc
    if x<minimum or (maximum is not None and x>maximum): raise ContractError(f"{label} outside range")
    return x
def number(v:Any,label:str,minimum:float|None=None,maximum:float|None=None)->float:
    try: x=float(v)
    except Exception as exc: raise ContractError(f"{label} not numeric") from exc
    if not (x==x and abs(x)!=float("inf")): raise ContractError(f"{label} non-finite")
    if minimum is not None and x<minimum: raise ContractError(f"{label} below minimum")
    if maximum is not None and x>maximum: raise ContractError(f"{label} above maximum")
    return x
def timestamp(v:Any,label:str)->str:
    x=text(v,label)
    try: datetime.fromisoformat(x.replace("Z","+00:00"))
    except Exception as exc: raise ContractError(f"{label} invalid ISO timestamp") from exc
    return x

def ordered_before(a:str,b:str,label:str):
    aa=datetime.fromisoformat(a.replace("Z","+00:00")); bb=datetime.fromisoformat(b.replace("Z","+00:00"))
    if aa>bb: raise ContractError(f"{label} temporal order failure")

@dataclass(frozen=True)
class UpstreamIntake:
    required_phase:str; exact_version:str; certificate_hash:str; certificate_id:str; handoff_hash:str; handoff_id:str; immutable:bool; hash_verified:bool; online_fdr_reference_accepted:bool; protected_evidence_access_zero:bool; research_only:bool
    @classmethod
    def parse(cls,v):
        req={"required_phase","exact_version","certificate_hash","certificate_id","handoff_hash","handoff_id","immutable","hash_verified","online_fdr_reference_accepted","protected_evidence_access_zero","research_only"}; exact(v,req,"upstream_intake")
        out=cls(text(v["required_phase"],"required_phase"),text(v["exact_version"],"exact_version"),text(v["certificate_hash"],"certificate_hash"),text(v["certificate_id"],"certificate_id"),text(v["handoff_hash"],"handoff_hash"),text(v["handoff_id"],"handoff_id"),*[boolean(v[k],k) for k in ["immutable","hash_verified","online_fdr_reference_accepted","protected_evidence_access_zero","research_only"]])
        if out.required_phase!="SAED_V4_28" or out.exact_version!="1.0.0": raise ContractError("V4-29 requires exact V4-28 v1.0.0")
        if not all([out.immutable,out.hash_verified,out.online_fdr_reference_accepted,out.protected_evidence_access_zero,out.research_only]): raise ContractError("unsafe upstream intake")
        return out

@dataclass(frozen=True)
class AirGapPolicy:
    exact_version:str; research_only:bool; default_deny:bool; network_access:bool; package_installation:bool; interactive_debugging:bool; shell_escape:bool; one_shot_required:bool; immutable_submission_required:bool; sealed_evaluator_required:bool; raw_result_release:bool; researcher_hidden_label_access:bool; researcher_key_share_access:bool; maximum_evaluations:int; maximum_round_trips:int; fail_closed_action:str; deterministic:bool
    @classmethod
    def parse(cls,v):
        req={"exact_version","research_only","default_deny","network_access","package_installation","interactive_debugging","shell_escape","one_shot_required","immutable_submission_required","sealed_evaluator_required","raw_result_release","researcher_hidden_label_access","researcher_key_share_access","maximum_evaluations","maximum_round_trips","fail_closed_action","deterministic"}; exact(v,req,"air_gap_policy")
        out=cls(text(v["exact_version"],"exact_version"),*[boolean(v[k],k) for k in ["research_only","default_deny","network_access","package_installation","interactive_debugging","shell_escape","one_shot_required","immutable_submission_required","sealed_evaluator_required","raw_result_release","researcher_hidden_label_access","researcher_key_share_access"]],integer(v["maximum_evaluations"],"maximum_evaluations",0,1),integer(v["maximum_round_trips"],"maximum_round_trips",0,0),text(v["fail_closed_action"],"fail_closed_action"),boolean(v["deterministic"],"deterministic"))
        if not (out.research_only and out.default_deny and out.one_shot_required and out.immutable_submission_required and out.sealed_evaluator_required and out.deterministic): raise ContractError("mandatory air-gap controls disabled")
        if any([out.network_access,out.package_installation,out.interactive_debugging,out.shell_escape,out.raw_result_release,out.researcher_hidden_label_access,out.researcher_key_share_access]): raise ContractError("forbidden air-gap capability enabled")
        if out.maximum_evaluations!=1 or out.maximum_round_trips!=0 or out.fail_closed_action!="quarantine": raise ContractError("air-gap budget must be one-shot and fail closed")
        return out

def parse_topology(v):
    req={"topology_id","zones","flows","network_egress_default","removable_media_policy","clock_policy","environment_capture","frozen_at"}; exact(v,req,"air_gap_topology")
    if v["network_egress_default"]!="deny" or v["removable_media_policy"]!="signed_one_way_receipt_only" or v["clock_policy"]!="fixed_reference_clock" or v["environment_capture"] is not True: raise ContractError("unsafe topology policy")
    zones=[]; zreq={"zone_id","role","researcher_access","custodian_access","evaluator_access","network_access","stores_plaintext_hidden_data"}; ids=set()
    for z in v["zones"]:
        exact(z,zreq,"zone"); zid=text(z["zone_id"],"zone_id")
        if zid in ids: raise ContractError("duplicate zone")
        for k in ["researcher_access","custodian_access","evaluator_access","network_access","stores_plaintext_hidden_data"]: boolean(z[k],k)
        zones.append(dict(z)); ids.add(zid)
    required={"research","transfer","sealed_evaluator","custody"}
    if ids!=required: raise ContractError("topology must contain exact required zones")
    by={z["zone_id"]:z for z in zones}
    if by["research"]["stores_plaintext_hidden_data"] or by["research"]["network_access"] or by["sealed_evaluator"]["network_access"] or not by["sealed_evaluator"]["stores_plaintext_hidden_data"]: raise ContractError("topology access escape")
    flows=[]; freq={"flow_id","source_zone","destination_zone","payload_class","direction","signed_receipt_required","raw_hidden_data_allowed","maximum_uses"}
    for f in v["flows"]:
        exact(f,freq,"flow");
        if f["source_zone"] not in ids or f["destination_zone"] not in ids: raise ContractError("unknown flow zone")
        if f["signed_receipt_required"] is not True or f["raw_hidden_data_allowed"] is not False or integer(f["maximum_uses"],"maximum_uses",1,1)!=1: raise ContractError("unsafe flow")
        flows.append(dict(f))
    if len(flows)!=3: raise ContractError("exactly three one-way flows required")
    return {**dict(v),"zones":sorted(zones,key=lambda x:x["zone_id"]),"flows":sorted(flows,key=lambda x:x["flow_id"]),"frozen_at":timestamp(v["frozen_at"],"frozen_at")}

def parse_custody_policy(v):
    req={"policy_id","minimum_custodians","threshold","researcher_may_be_custodian","evaluator_may_export_plaintext","key_shares_exportable","dual_control_required","immutable","synthetic_fixture_only"}; exact(v,req,"custody_policy")
    out=dict(v); out["minimum_custodians"]=integer(v["minimum_custodians"],"minimum_custodians",2); out["threshold"]=integer(v["threshold"],"threshold",2)
    if out["threshold"]>out["minimum_custodians"]: raise ContractError("custody threshold exceeds custodian count")
    if v["researcher_may_be_custodian"] or v["evaluator_may_export_plaintext"] or v["key_shares_exportable"] or v["dual_control_required"] is not True or v["immutable"] is not True or v["synthetic_fixture_only"] is not True: raise ContractError("unsafe custody policy")
    return out

def parse_protocol(v):
    req={"protocol_id","locked_at","random_seed","metric_specs","pass_rule","baseline_id","deterministic","adaptive_changes_allowed","maximum_evaluations","tolerance","disclosure_policy_id"}; exact(v,req,"evaluation_protocol")
    specs=[]; sreq={"metric","direction","weight","minimum","maximum","required"}; seen=set()
    for x in v["metric_specs"]:
        exact(x,sreq,"metric_spec"); metric=text(x["metric"],"metric")
        if metric not in METRICS or metric in seen: raise ContractError("invalid metric registry")
        specs.append({**dict(x),"weight":number(x["weight"],"weight",0.0,1.0),"minimum":number(x["minimum"],"minimum"),"maximum":number(x["maximum"],"maximum"),"required":boolean(x["required"],"required")}); seen.add(metric)
    if seen!=set(METRICS): raise ContractError("metric registry incomplete")
    pr=v["pass_rule"]; preq={"minimum_balanced_accuracy","maximum_brier_score","minimum_delta_vs_baseline","all_required"}; exact(pr,preq,"pass_rule")
    if pr["all_required"] is not True: raise ContractError("pass rule must require all gates")
    if v["deterministic"] is not True or v["adaptive_changes_allowed"] is not False or integer(v["maximum_evaluations"],"maximum_evaluations",1,1)!=1: raise ContractError("protocol not one-shot deterministic")
    out=dict(v); out["locked_at"]=timestamp(v["locked_at"],"locked_at"); out["random_seed"]=integer(v["random_seed"],"random_seed",0); out["tolerance"]=number(v["tolerance"],"tolerance",0.0,1e-6); out["metric_specs"]=sorted(specs,key=lambda x:x["metric"])
    return out

def parse_disclosure(v):
    req={"policy_id","allowed_fields","forbidden_fields","metric_precision","minimum_group_size","release_mode","raw_rows_allowed","per_record_outputs_allowed","confusion_matrix_allowed","exact_thresholds_released","immutable"}; exact(v,req,"disclosure_policy")
    allowed=[text(x,"allowed_field") for x in v["allowed_fields"]]; forbidden=[text(x,"forbidden_field") for x in v["forbidden_fields"]]
    if set(allowed)!={"evaluation_id","candidate_id","dataset_commitment_hash","protocol_id","decision","aggregate_metrics","baseline_comparison","release_hash"}: raise ContractError("disclosure allowlist mismatch")
    if not FORBIDDEN_DISCLOSURE_FIELDS.issubset(set(forbidden)): raise ContractError("disclosure denylist incomplete")
    if integer(v["metric_precision"],"metric_precision",0,4)>4 or integer(v["minimum_group_size"],"minimum_group_size",20)<20: raise ContractError("unsafe disclosure granularity")
    if v["release_mode"]!="aggregate_redacted_once" or v["raw_rows_allowed"] or v["per_record_outputs_allowed"] or v["confusion_matrix_allowed"] or v["exact_thresholds_released"] or v["immutable"] is not True: raise ContractError("unsafe disclosure policy")
    return {**dict(v),"allowed_fields":sorted(allowed),"forbidden_fields":sorted(forbidden)}

def parse_config(v):
    req={"upstream_intake","air_gap_policy","air_gap_topology","custody_policy","evaluation_protocol","disclosure_policy"}; exact(v,req,"full_config")
    protocol=parse_protocol(v["evaluation_protocol"]); disclosure=parse_disclosure(v["disclosure_policy"])
    if protocol["disclosure_policy_id"]!=disclosure["policy_id"]: raise ContractError("protocol disclosure binding mismatch")
    return {"upstream_intake":UpstreamIntake.parse(v["upstream_intake"]),"air_gap_policy":AirGapPolicy.parse(v["air_gap_policy"]),"air_gap_topology":parse_topology(v["air_gap_topology"]),"custody_policy":parse_custody_policy(v["custody_policy"]),"evaluation_protocol":protocol,"disclosure_policy":disclosure}

def parse_custody_manifest(v,policy):
    req={"dataset_id","dataset_version","encrypted_blob_hash","plaintext_commitment_hash","schema_hash","row_count","feature_count","label_columns","custodian_ids","threshold","key_share_commitments","storage_zone","created_at","synthetic_fixture","researcher_read_access","evaluator_read_access","immutable"}; exact(v,req,"custody_manifest")
    custodians=[text(x,"custodian_id") for x in v["custodian_ids"]]
    if len(custodians)!=len(set(custodians)) or len(custodians)<policy["minimum_custodians"] or integer(v["threshold"],"threshold",2)!=policy["threshold"]: raise ContractError("custodian threshold failure")
    shares=v["key_share_commitments"]
    if set(shares)!=set(custodians) or any(not isinstance(x,str) or len(x)!=64 for x in shares.values()): raise ContractError("key share commitments invalid")
    if v["storage_zone"]!="custody" or v["synthetic_fixture"] is not True or v["researcher_read_access"] is not False or v["evaluator_read_access"] is not True or v["immutable"] is not True: raise ContractError("custody access violation")
    out=dict(v); out["row_count"]=integer(v["row_count"],"row_count",20); out["feature_count"]=integer(v["feature_count"],"feature_count",1); out["created_at"]=timestamp(v["created_at"],"created_at"); out["custodian_ids"]=sorted(custodians)
    if not v["label_columns"]: raise ContractError("hidden label column required")
    return out

def parse_candidate(v):
    req={"candidate_id","candidate_version","model_artifact_hash","preprocessing_hash","feature_contract_hash","inference_entrypoint","model_spec","training_data_roles","network_dependencies","submitted_at","submitter_actor_id","frozen","hidden_data_touched","adaptive_to_final_evaluation","source_commit_hash"}; exact(v,req,"candidate_submission")
    ms=v["model_spec"]; exact(ms,{"model_type","weights","intercept","link","feature_order"},"model_spec")
    if ms["model_type"]!="deterministic_logistic_reference" or ms["link"]!="sigmoid": raise ContractError("unsupported sealed reference model")
    weights=[number(x,"weight",-100,100) for x in ms["weights"]]; features=[text(x,"feature") for x in ms["feature_order"]]
    if len(weights)!=len(features) or len(features)!=len(set(features)) or not features: raise ContractError("model feature contract invalid")
    roles=[text(x,"training_role") for x in v["training_data_roles"]]
    if not roles or any(x not in ALLOWED_TRAINING_ROLES for x in roles): raise ContractError("forbidden training data role")
    if v["network_dependencies"]!=[] or v["frozen"] is not True or v["hidden_data_touched"] is not False or v["adaptive_to_final_evaluation"] is not False: raise ContractError("candidate not irreversibly clean")
    out=dict(v); out["submitted_at"]=timestamp(v["submitted_at"],"submitted_at"); out["model_spec"]={**dict(ms),"weights":weights,"intercept":number(ms["intercept"],"intercept",-100,100),"feature_order":features}; out["training_data_roles"]=sorted(roles)
    return out

def parse_fixture(v,manifest):
    req={"fixture_id","dataset_id","dataset_version","classification","synthetic_fixture","schema_hash","records","sealed_at","future_suffix_records"}; exact(v,req,"sealed_fixture")
    if v["dataset_id"]!=manifest["dataset_id"] or v["dataset_version"]!=manifest["dataset_version"] or v["classification"]!="sealed_synthetic_hidden_evaluation" or v["synthetic_fixture"] is not True: raise ContractError("fixture classification failure")
    recs=[]; rreq={"record_id","features","hidden_label","segment"}; seen=set()
    for r in v["records"]:
        exact(r,rreq,"sealed_record"); rid=text(r["record_id"],"record_id")
        if rid in seen: raise ContractError("duplicate sealed record")
        features={text(k,"feature_name"):number(val,"feature_value",-1e9,1e9) for k,val in r["features"].items()}
        label=integer(r["hidden_label"],"hidden_label",0,1); recs.append({"record_id":rid,"features":features,"hidden_label":label,"segment":text(r["segment"],"segment")}); seen.add(rid)
    if len(recs)!=manifest["row_count"]: raise ContractError("fixture row count mismatch")
    suffix=[]
    for r in v["future_suffix_records"]:
        exact(r,rreq,"future_suffix_record"); suffix.append(dict(r))
    return {**dict(v),"records":sorted(recs,key=lambda x:x["record_id"]),"sealed_at":timestamp(v["sealed_at"],"sealed_at"),"future_suffix_records":suffix}
