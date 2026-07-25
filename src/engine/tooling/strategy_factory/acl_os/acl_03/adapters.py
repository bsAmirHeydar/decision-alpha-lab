from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id

def compile_adapter_contracts(package:dict[str,Any],known_time_ir:dict[str,Any],feature_ir:dict[str,Any])->list[dict[str,Any]]:
    cid=package["manifest"]["context_id"]; cv=package["manifest"]["context_version"]; out=[]
    for src in sorted(package["data"].get("sources",[]),key=lambda x:x["source_id"]):
        body={"schema_version":"1.0.0","adapter_id":stable_id("ADP",cid,cv,"DATA_SOURCE",src["source_id"]),"adapter_kind":"DATA_SOURCE","context_id":cid,"source_id":src["source_id"],"artifact_ref":src["artifact_ref"],"required_methods":["read_snapshot","fingerprint","validate_schema","validate_known_time","health"],"capabilities":{"network_egress":"DENY_BY_DEFAULT","filesystem_write":"DECLARED_CACHE_ONLY","secret_access":"NAMED_SECRET_ONLY","order_submission":False,"capital_access":False},"known_time_field":src["known_time_field"],"freshness_slo_ms":src["freshness_slo_ms"],"classification":src["classification"],"implementation_status":"CONTRACT_ONLY"}
        out.append({**body,"contract_digest":digest_object(body)})
    cal=package["causal_clock"]
    body={"schema_version":"1.0.0","adapter_id":stable_id("ADP",cid,cv,"CALENDAR",cal["calendar_id"]),"adapter_kind":"CALENDAR","context_id":cid,"calendar_id":cal["calendar_id"],"required_methods":["resolve_session","normalize_time","is_open","next_boundary"],"capabilities":{"network_egress":"DENY_BY_DEFAULT","filesystem_write":"NONE","secret_access":"NONE","order_submission":False,"capital_access":False},"implementation_status":"CONTRACT_ONLY"}
    out.append({**body,"contract_digest":digest_object(body)})
    for b in feature_ir["bindings"]:
        body={"schema_version":"1.0.0","adapter_id":stable_id("ADP",cid,cv,"FEATURE_VIEW",b["view_id"]),"adapter_kind":"FEATURE_VIEW","context_id":cid,"view_id":b["view_id"],"required_methods":["materialize","validate_known_time","missingness_vector","freshness_vector"],"capabilities":{"network_egress":"NONE","filesystem_write":"DECLARED_OUTPUT_ONLY","secret_access":"NONE","order_submission":False,"capital_access":False},"implementation_status":"CONTRACT_ONLY"}
        out.append({**body,"contract_digest":digest_object(body)})
    return out
