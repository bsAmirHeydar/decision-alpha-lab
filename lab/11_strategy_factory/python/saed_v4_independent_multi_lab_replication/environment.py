from __future__ import annotations
from .canonical import content_hash,stable_id
from .contracts import require_exact
from .errors import SecurityError

FIELDS=["environment_id","os_family","runtime","runtime_version","dependency_lock_hash","container_or_vm_image_hash","cpu_architecture","timezone","locale","network_access","package_installation","interactive_shell","mutable_clock","shared_mutable_state","captured_at","synthetic_fixture"]

def attest(values:list[dict],registry:dict)->dict:
    by_id={v["environment_id"]:v for v in values}; out=[]
    for lab in registry["labs"]:
        value=by_id.get(lab["environment_id"])
        if value is None: raise SecurityError("environment missing")
        require_exact(value,FIELDS,name="environment_attestation")
        for field in ["network_access","package_installation","interactive_shell","mutable_clock","shared_mutable_state"]:
            if value[field] is not False: raise SecurityError(f"{field} must be false")
        if value["synthetic_fixture"] is not True: raise SecurityError("synthetic marker required")
        body=dict(value); body["lab_id"]=lab["lab_id"]; body["attestation_id"]=stable_id("v430_environment",body); body["attestation_hash"]=content_hash(body); out.append(body)
    report={"phase":"SAED_V4_30","attestations":out,"attestation_count":len(out),"default_deny_verified":True,"distinct_environment_ids":len({x["environment_id"] for x in out})==len(out),"research_only":True}
    report["report_id"]=stable_id("v430_environments",report); report["report_hash"]=content_hash(report); return report
