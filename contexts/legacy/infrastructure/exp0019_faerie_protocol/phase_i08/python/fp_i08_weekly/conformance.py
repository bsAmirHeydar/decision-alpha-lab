from .registry import CONTRACTS,REASONS,contract_registry_hash,reason_registry_hash
def run_conformance():
    checks={
      "contract_count":len(CONTRACTS)==15,
      "reason_count":len(REASONS)>=13,
      "contract_hash":len(contract_registry_hash())==64,
      "reason_hash":len(reason_registry_hash())==64,
      "owner_ww_reasons_present":all(x in REASONS for x in ("FP_RC_WW_NEUTRALIZED","FP_RC_WW_DATA_INCOMPLETE","FP_RC_WW_NONE_ALLOW_BOTH","FP_RC_SUPPRESSED_BY_WW")),
    }
    return {"passed":all(checks.values()),"checks":checks}
