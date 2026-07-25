from .canonical import content_id,digest_object
from .registries import EXTRACTION_GATES

def _risk(c):
    f=c["flags"]
    if f["order_api"] or f["network_api"]:return "CRITICAL_EXECUTION"
    if f["object_mutation_api"] or f["file_write_api"] or f["global_variable_api"]:return "HIGH_SIDE_EFFECT"
    if c["category"] in ("STATE_STREAM","REFERENCE_LIFECYCLE","CLOSED_BAR_CLOCK"):return "MEDIUM_STATEFUL"
    return "LOW_PURE"
def _status(c):
    f=c["flags"]
    if f["order_api"] or f["network_api"] or f["file_write_api"]:return "BLOCKED_SECURITY_SENSITIVE"
    if f["object_mutation_api"] or f["global_variable_api"]:return "BLOCKED_SIDE_EFFECT_REVIEW"
    if f["current_bar_access"]:return "BLOCKED_KNOWN_TIME_REVIEW"
    if c["signature_count"]>1:return "BLOCKED_SIGNATURE_VARIANCE"
    if c["category"]=="DOMAIN_LOGIC":return "BLOCKED_DOMAIN_SEMANTICS"
    return "STATIC_EQUIVALENCE_PROVEN_RUNTIME_UNKNOWN"
def variance(c):
    dims=[]
    names=sorted({m["function_name"] for m in c["members"]}); families=c["families"]
    vals={
      "FUNCTION_NAME":names,"RETURN_TYPE":sorted({m["return_type"] for m in c["members"]}),"PARAMETER_ARITY":sorted({m["parameter_arity"] for m in c["members"]}),"PARAMETER_TYPES":[s["parameter_types"] for s in c["signatures"]],"PARAMETER_NAMES":[m["parameter_text"] for m in c["members"]],"PATH_FAMILY":families,
      "CURRENT_BAR_ACCESS":[c["flags"]["current_bar_access"]],"SIDE_EFFECT_SURFACE":[k for k,v in c["flags"].items() if v],"EXECUTION_AUTHORITY":[c["flags"]["order_api"] or c["flags"]["network_api"]],"TIMEFRAME_SCOPE":[c["flags"]["timeframe_api"]],"SESSION_BOUNDARY":[c["flags"]["session_or_dst"]]
    }
    for d,v in vals.items():
        dims.append({"dimension":d,"observed_values":v,"review_status":"PASS_STATIC" if len({str(x) for x in v})<=1 else "REVIEW_REQUIRED"})
    o={"schema_version":"1.0.0","variance_id":content_id("VAR",[c["candidate_id"],dims]),"candidate_id":c["candidate_id"],"dimensions":dims,"approved_parameterization":[],"flag_explosion_rejected":True,"variance_digest":None};o["variance_digest"]=digest_object(o,"variance_digest");return o
def equivalence(c):
    status=_status(c); risk=_risk(c); gates=[]
    for g in EXTRACTION_GATES:
        s="PASS";reason=None
        if g=="SIGNATURE_REVIEW" and c["signature_count"]>1:s="BLOCKED";reason="SIGNATURE_VARIANCE_REQUIRES_REVIEW"
        elif g=="KNOWN_TIME_REVIEW" and c["flags"]["current_bar_access"]:s="BLOCKED";reason="CURRENT_BAR_EVIDENCE_REQUIRES_REVIEW"
        elif g=="SIDE_EFFECT_REVIEW" and (c["flags"]["object_mutation_api"] or c["flags"]["file_write_api"] or c["flags"]["global_variable_api"]):s="BLOCKED";reason="OBJECT_SIDE_EFFECT_REQUIRES_REVIEW"
        elif g=="NO_DOMAIN_RULE" and c["category"]=="DOMAIN_LOGIC":s="BLOCKED";reason="DOMAIN_RULE_DETECTED"
        elif g=="OWNER_APPROVAL":s="UNKNOWN";reason="OWNER_APPROVAL_UNKNOWN"
        elif g=="INDEPENDENT_REVIEW":s="UNKNOWN";reason="INDEPENDENT_REVIEW_UNKNOWN"
        elif g=="MQL5_COMPILE":s="UNKNOWN";reason="MQL5_COMPILATION_UNKNOWN"
        elif g in ("RUNTIME_PARITY","CONSUMER_REGRESSION","RESTART_PARITY"):s="UNKNOWN";reason="RUNTIME_PARITY_UNKNOWN"
        elif g=="MISSING_DATA_FAIL_CLOSED" and c["category"] in ("STATE_STREAM","CLOSED_BAR_CLOCK","TIME_SESSION_CONFIGURATION"):s="UNKNOWN";reason="RUNTIME_PARITY_UNKNOWN"
        gates.append({"gate":g,"status":s,"reason_code":reason})
    o={"schema_version":"1.0.0","equivalence_id":content_id("EQUIV",c["candidate_id"]),"candidate_id":c["candidate_id"],"risk_class":risk,"evidence_status":status,"static_normalized_body_equal":True,"source_hashes_bound":True,"runtime_equivalence_proven":False,"extraction_authorized":False,"non_compensatory_gates":gates,"equivalence_digest":None};o["equivalence_digest"]=digest_object(o,"equivalence_digest");return o
def design(c,e):
    target_slug=c["category"].lower(); engine_id=content_id("ENG",[c["normalized_body_sha256"],c["category"]])
    o={"schema_version":"1.0.0","engine_id":engine_id,"candidate_id":c["candidate_id"],"category":c["category"],"version":"0.1.0-proposed","design_state":"REFERENCE_DESIGN_ONLY","target_python_path":f"lab/11_strategy_factory/shared_engines/{engine_id}/","target_mql5_path":f"mql5/Include/AlphaLab/ContextOS/Shared/{engine_id}/","materialized":False,"implementation_source_selected":False,"consumer_count":c["consumer_count"],"consumer_families":c["families"],"allowed_variance":[],"forbidden_design_patterns":["GIANT_FLAG_ENGINE","DOMAIN_RULE_IN_SHARED_ENGINE","HIDDEN_CURRENT_BAR_DEFAULT","EXECUTION_AUTHORITY","MUTABLE_GLOBAL_SINGLETON"],"rollback_strategy":"retain original consumers and wrappers; no source mutation in LCM-07","extraction_authorized":False,"evidence_status":e["evidence_status"],"design_digest":None};o["design_digest"]=digest_object(o,"design_digest");return o
def adapters(c,d):
    out=[]
    for m in c["members"]:
        o={"schema_version":"1.0.0","adapter_id":content_id("ENGADP",[d["engine_id"],m["artifact_path"],m["function_name"],m["line_start"]]),"engine_id":d["engine_id"],"candidate_id":c["candidate_id"],"consumer_artifact_path":m["artifact_path"],"consumer_artifact_sha256":m["artifact_sha256"],"legacy_function_name":m["function_name"],"adapter_type":"CONSUMER_NAME_WRAPPER_PROPOSAL","write_performed":False,"source_mutation_allowed":False,"semantic_expansion_allowed":False,"runtime_authority":False,"adapter_digest":None};o["adapter_digest"]=digest_object(o,"adapter_digest");out.append(o)
    return out
def governance(c,d,e):
    o={"schema_version":"1.0.0","governance_id":content_id("ENGGOV",d["engine_id"]),"engine_id":d["engine_id"],"candidate_id":c["candidate_id"],"owner_role":"ALPHA_LAB_SHARED_ENGINE_STEWARD","named_owner":"UNKNOWN_BLOCKING","independent_reviewer_role":"ALPHA_LAB_MIGRATION_REVIEWER","named_reviewer":"UNKNOWN_BLOCKING","version":"0.1.0-proposed","compatibility_source_hashes":sorted({m["artifact_sha256"] for m in c["members"]}),"extension_contract":{"new_consumer_requires_equivalence":True,"semantic_change_requires_major_version":True,"runtime_change_requires_replay":True,"execution_authority_forbidden":True},"approval_state":"PENDING_HUMAN_APPROVAL","extraction_authorized":False,"governance_digest":None};o["governance_digest"]=digest_object(o,"governance_digest");return o
def decision(c,e,d,g):
    if e["evidence_status"]=="BLOCKED_SECURITY_SENSITIVE":state="CANDIDATE_REJECTED";disp="REJECT_SECURITY_SENSITIVE"
    elif e["evidence_status"] in ("BLOCKED_SIDE_EFFECT_REVIEW","BLOCKED_KNOWN_TIME_REVIEW","BLOCKED_SIGNATURE_VARIANCE","BLOCKED_DOMAIN_SEMANTICS"):state="CANDIDATE_HELD";disp="KEEP_LOCAL_PENDING_RUNTIME_PARITY"
    else:state="REFERENCE_DESIGN_ACCEPTED_EXTRACTION_BLOCKED";disp="DESIGN_REFERENCE_ONLY"
    o={"schema_version":"1.0.0","decision_id":content_id("ENGDEC",[c["candidate_id"],state]),"candidate_id":c["candidate_id"],"engine_id":d["engine_id"],"decision_state":state,"disposition":disp,"static_equivalence_proven":True,"runtime_equivalence_proven":False,"owner_approval":False,"independent_review":False,"mql5_compile_evidence":False,"materialization_authorized":False,"source_move_authorized":False,"source_delete_authorized":False,"merge_authorized":False,"decision_digest":None};o["decision_digest"]=digest_object(o,"decision_digest");return o
