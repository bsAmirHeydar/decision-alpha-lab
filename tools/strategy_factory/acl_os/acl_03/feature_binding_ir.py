from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id
from .types import Finding,Severity

def compile_feature_binding_ir(package:dict[str,Any])->tuple[dict[str,Any],list[dict[str,Any]]]:
    fv=package["feature_views"]; findings=[]; bindings=[]; seen=set()
    for view in sorted(fv.get("views",[]),key=lambda x:x["view_id"]):
        vid=view["view_id"]
        if vid in seen: findings.append(Finding("ACL03_DUPLICATE_FEATURE_VIEW",Severity.BLOCKER,"feature_views.views","duplicate feature view id","use a unique view_id",{"view_id":vid}).to_dict())
        seen.add(vid)
        if not view.get("known_time_safe",False): findings.append(Finding("ACL03_UNSAFE_FEATURE_VIEW",Severity.BLOCKER,f"feature_views.{vid}","feature view is not declared known-time safe","make the view known-time safe or remove it").to_dict())
        bindings.append({"binding_id":stable_id("FVB",package["manifest"]["context_id"],vid),"view_id":vid,"kind":view["kind"],"fields":list(view.get("fields",[])),"schema_ref":view["schema_ref"],"known_time_safe":bool(view["known_time_safe"]),"missingness_vector":view["missingness_vector"],"freshness_vector":view["freshness_vector"],"runtime_order":len(bindings)})
    body={"schema_version":"1.0.0","context_id":package["manifest"]["context_id"],"context_version":package["manifest"]["context_version"],"bindings":bindings,"fusion_policy":fv["fusion_policy"],"missing_view_policy":fv["missing_view_policy"],"feature_order_frozen":True}
    return {**body,"feature_binding_ir_digest":digest_object(body)},findings
