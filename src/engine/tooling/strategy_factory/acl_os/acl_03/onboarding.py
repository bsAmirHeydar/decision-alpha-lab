from __future__ import annotations
from typing import Any
from .canonical import digest_object

def build_onboarding_report(package:dict[str,Any],prereq:dict[str,Any],findings:list[dict[str,Any]],replay:dict[str,Any],adapters:list[dict[str,Any]],artifact_count:int)->dict[str,Any]:
    blockers=[f for f in findings if f["severity"] in {"BLOCKER","ERROR"}]
    contract_only=[a["adapter_id"] for a in adapters if a.get("implementation_status")!="IMPLEMENTED_AND_QUALIFIED"]
    gates={
      "source_frozen":{"passed":True,"reason_codes":[]},
      "authority_bound":{"passed":prereq["passed"],"reason_codes":[] if prereq["passed"] else ["ACL03_PREREQUISITES_FAILED"]},
      "ir_compiled":{"passed":not blockers,"reason_codes":sorted({f["code"] for f in blockers})},
      "golden_replay":{"passed":replay.get("failed_count",1)==0 and replay.get("case_count",0)>0,"reason_codes":[] if replay.get("failed_count",1)==0 and replay.get("case_count",0)>0 else ["ACL03_GOLDEN_REPLAY_FAILED"]},
      "adapter_contracts":{"passed":len(adapters)>0,"reason_codes":[] if adapters else ["ACL03_ADAPTER_CONTRACTS_MISSING"]},
      "adapter_implementation":{"passed":not contract_only,"reason_codes":[] if not contract_only else ["ACL03_ADAPTER_IMPLEMENTATION_REQUIRED"]},
      "external_data_qualification":{"passed":False,"reason_codes":["ACL14_REAL_CONTEXT_EVIDENCE_REQUIRED"]},
      "research_entry":{"passed":False,"reason_codes":["ACL04_SETUP_FACTORY_REQUIRED","ACL05_IMMUTABLE_BATCH_REQUIRED"]},
      "live_activation":{"passed":False,"reason_codes":["ACL11_RUNTIME_PARITY_REQUIRED","ACL12_SECURITY_HARDENING_REQUIRED","ACL14_CAPITAL_AUTHORIZATION_REQUIRED"]},
    }
    compiled=all(gates[x]["passed"] for x in ("source_frozen","authority_bound","ir_compiled","golden_replay","adapter_contracts"))
    body={"schema_version":"1.0.0","context_id":package["manifest"]["context_id"],"context_version":package["manifest"]["context_version"],"decision":"COMPILED_WITH_OBLIGATIONS" if compiled else "REJECT","highest_state":"CONTEXT_COMPILED" if compiled else "ONBOARDING_BLOCKED","gates":gates,"open_obligations":[{"code":"ACL03_ADAPTER_IMPLEMENTATION_REQUIRED","subject_ids":contract_only},{"code":"ACL04_DUAL_SETUP_FACTORY_REQUIRED","subject_ids":[]},{"code":"ACL05_IMMUTABLE_BATCH_REQUIRED","subject_ids":[]}],"allowed_next_actions":["IMPLEMENT_REGISTERED_ADAPTERS","ADD_DOMAIN_GOLDEN_CASES","REQUEST_ACL04_SETUP_SEARCH_AUTHORITY"] if compiled else ["REMEDIATE_COMPILATION_FINDINGS"],"generated_artifact_count":artifact_count,"claim_ceiling":"CONTEXT_COMPILATION_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
    return {**body,"report_digest":digest_object(body)}
