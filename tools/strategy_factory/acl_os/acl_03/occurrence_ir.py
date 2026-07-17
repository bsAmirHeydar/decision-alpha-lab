from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id
from .types import Finding,Severity

REQUIRED_IDENTITY={"context_id","context_version","anchor_time","direction","subject_key"}

def compile_occurrence_ir(package:dict[str,Any])->tuple[dict[str,Any],list[dict[str,Any]]]:
    raw=package["occurrence"]; cid=package["manifest"]["context_id"]; cv=package["manifest"]["context_version"]
    fields=list(raw.get("identity_fields",[])); findings=[]
    missing=sorted(REQUIRED_IDENTITY-set(fields))
    if missing: findings.append(Finding("ACL03_OCCURRENCE_IDENTITY_INCOMPLETE",Severity.BLOCKER,"occurrence.identity_fields","occurrence identity omits required fields","add all required immutable identity fields",{"missing":missing}).to_dict())
    recipe={"algorithm":"SHA256_CANONICAL_JSON","ordered_fields":fields,"namespace":f"{cid}@{cv}","revision_policy":raw.get("revision_policy")}
    body={"schema_version":"1.0.0","context_id":cid,"context_version":cv,"occurrence_type_id":stable_id("OCC_TYPE",cid,cv),"identity_recipe":recipe,"start_rule":raw.get("start_rule"),"confirmation_rule":raw.get("confirmation_rule"),"invalidation_rule":raw.get("invalidation_rule"),"expiry_rule":raw.get("expiry_rule"),"deduplication_rule":raw.get("deduplication_rule"),"precedence":list(raw.get("precedence",[])),"revision_policy":raw.get("revision_policy"),"append_only":True}
    return {**body,"occurrence_ir_digest":digest_object(body)},findings

def build_occurrence_id(ir:dict[str,Any],values:dict[str,Any])->str:
    fields=ir["identity_recipe"]["ordered_fields"]
    missing=[x for x in fields if x not in values]
    if missing: raise ValueError(f"missing occurrence identity fields: {missing}")
    return stable_id("OCC",ir["identity_recipe"]["namespace"],*[str(values[x]) for x in fields])
