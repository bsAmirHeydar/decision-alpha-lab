from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique
from .errors import LicenseError
from .canonical import seal

def freeze_policy(v:dict)->dict:
    require_exact(v,["policy_id","allowed_licenses","restricted_licenses","forbidden_licenses","unknown_license_action","copyleft_action","commercial_use_required","redistribution_review_required"])
    for k in ["allowed_licenses","restricted_licenses","forbidden_licenses"]:
        if sorted(set(v[k]))!=v[k]: raise LicenseError(f"{k} must be sorted unique")
    if set(v["allowed_licenses"])&set(v["forbidden_licenses"]): raise LicenseError("license sets overlap")
    if v["unknown_license_action"]!="QUARANTINE": raise LicenseError("unknown licenses must quarantine")
    return seal(deepcopy(v)|{"phase":"SAED_V4_35","research_only":True},"v435_license_policy","policy_receipt_id","policy_hash")

def review(sbom:dict,policy:dict)->dict:
    allowed=set(policy["allowed_licenses"]); restricted=set(policy["restricted_licenses"]); forbidden=set(policy["forbidden_licenses"]); rows=[]; blocked=False
    for c in sbom["components"]:
        lic=c["license_id"]; decision="ALLOW"
        if lic in forbidden or lic not in allowed|restricted: decision="QUARANTINE"; blocked=True
        elif lic in restricted: decision="REVIEW_REQUIRED"
        rows.append({"component_id":c["component_id"],"license_id":lic,"decision":decision,"commercial_use_compatible":lic not in forbidden,"redistribution_review_required":decision!="ALLOW"})
    return seal({"phase":"SAED_V4_35","reviews":rows,"component_count":len(rows),"blocked":blocked,"all_licenses_known":all(r["license_id"]!="UNKNOWN" for r in rows),"research_only":True},"v435_license_review","review_id","review_hash")
