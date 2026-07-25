from __future__ import annotations
from datetime import datetime
from typing import Any
from .budget import ResearchLedger
from .canonical import content_hash, stable_id
from .contracts import MechanismDatasetContract, REQUIRED_RECORD_FIELDS
from .errors import ContractError, KnownTimeError

def ts(value:str)->datetime: return datetime.fromisoformat(value.replace("Z","+00:00"))
def validate(records:list[dict[str,Any]], contract:MechanismDatasetContract, ledger:ResearchLedger)->dict[str,Any]:
    if len(records)<contract.minimum_records: raise ContractError("insufficient records")
    ledger.consume("records",len(records),{"purpose":"frozen_mechanism_dataset_validation"})
    ids=set(); roles={}; models=set(); contexts=set(); cluster_roles={}
    for r in records:
        if set(r)!=REQUIRED_RECORD_FIELDS: raise ContractError("record field mismatch")
        if r["record_id"] in ids: raise ContractError("duplicate record")
        ids.add(r["record_id"]); roles[r["role"]]=roles.get(r["role"],0)+1; models.add(r["model_id"]); contexts.add(r["context_id"]); cluster_roles.setdefault(r["cluster_id"],set()).add(r["role"])
        if r["role"] not in contract.allowed_roles: raise ContractError("unknown role")
        if ts(r["known_time"])>ts(r["decision_time"]): raise KnownTimeError("feature known after decision")
        if ts(r["decision_time"])>ts(r["outcome_observed_at"]): raise KnownTimeError("outcome observed before decision")
        if r["future_suffix_accessed"] or r["protected_evidence_accessed"]: raise KnownTimeError("forbidden evidence accessed")
        if not r["immutable_model"]: raise ContractError("mutable model")
        n=len(r["feature_names"])
        if not (n==len(r["feature_values"])==len(r["feature_weights"])==len(r["adaptation_deltas"])): raise ContractError("feature dimension mismatch")
        if len(r["view_names"])!=len(r["view_values"]) or len(r["view_values"])!=len(r["view_weights"]): raise ContractError("view dimension mismatch")
        if r["layer_ids"]!=["representation_1","representation_2"]: raise ContractError("layer registry mismatch")
        m1,m2=r["layer_matrices"]
        if any(len(row)!=n for row in m1) or any(len(row)!=len(m1) for row in m2) or len(r["output_weights"])!=len(m2): raise ContractError("network dimension mismatch")
        for source in r["transfer_sources"]:
            if ts(source["source_known_time"])>ts(r["decision_time"]): raise KnownTimeError("future transfer source")
    if len(models)<contract.minimum_models or len(contexts)<contract.minimum_contexts: raise ContractError("dataset diversity insufficient")
    if any(roles.get(role,0)<contract.minimum_records_per_role for role in contract.allowed_roles): raise ContractError("role support insufficient")
    if any(len(x)>1 for x in cluster_roles.values()): raise ContractError("cluster crosses evidence roles")
    payload={"phase":"SAED_V4_26","record_count":len(records),"model_count":len(models),"context_count":len(contexts),"cluster_count":len(cluster_roles),"role_counts":dict(sorted(roles.items())),"feature_registry":records[0]["feature_names"],"view_registry":records[0]["view_names"],"layer_registry":records[0]["layer_ids"],"immutable_models":True,"known_time_verified":True,"cluster_role_separation_verified":True,"dataset_hash":content_hash(records)}
    payload["dataset_summary_id"]=stable_id("mechanism_dataset",payload); payload["dataset_summary_hash"]=content_hash(payload)
    return payload
