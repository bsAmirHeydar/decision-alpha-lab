from __future__ import annotations
from pathlib import Path
from .canonical import stable_id,digest_object
from .constants import FORBIDDEN_BROKER_TOKENS
from .errors import AuthorityDenied
class AuthorityNegativeVerifier:
    def assert_mode_denied(self,adapter:dict,mode:str)->dict:
        if mode in {"PAPER","LIVE"}:raise AuthorityDenied(f"{mode} submission is forbidden")
        if mode!="DRY_RUN":raise AuthorityDenied(f"Unsupported mode: {mode}")
        return {"adapter_id":adapter["adapter_id"],"mode":mode,"submission_attempt_count":0,"result":"PASS"}
    def verify_adapter(self,adapter:dict)->dict:
        violations=[]
        checks={"submission_capability_default_false":adapter.get("submission_capability_default") is False,"live_mode_false":adapter.get("live_mode_allowed") is False,"paper_mode_false":adapter.get("paper_mode_allowed") is False,"broker_api_not_implemented":adapter.get("broker_api_invocation_implemented") is False,"context_recompute_false":adapter.get("context_recompute_allowed") is False,"setup_recompute_false":adapter.get("setup_recompute_allowed") is False}
        for k,v in checks.items():
            if not v:violations.append(k)
        result={"authority_result_id":stable_id("AUTHNEG",adapter["adapter_id"]),"adapter_id":adapter["adapter_id"],"source_path":adapter.get("source_path"),"checks":checks,"violations":violations,"runtime_attempts":{"DRY_RUN":"ZERO_SUBMISSION","PAPER":"DENIED","LIVE":"DENIED"},"live_order_count":0,"paper_order_count":0,"capital_activation_count":0,"result":"PASS" if not violations else "FAIL"}
        result["authority_result_digest"]=digest_object(result,"authority_result_digest")
        return result

def scan_canonical_tree(root:Path)->dict:
    hits=[]
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in {'.py','.mq5','.mqh','.cpp','.h','.hpp'}:continue
        text=path.read_text(encoding='utf-8',errors='ignore')
        for token in FORBIDDEN_BROKER_TOKENS:
            for n,line in enumerate(text.splitlines(),1):
                if token in line:hits.append({"path":path.as_posix(),"line":n,"token":token})
    return {"scanned_root":root.as_posix(),"hits":hits,"hit_count":len(hits),"result":"PASS" if not hits else "FAIL"}
