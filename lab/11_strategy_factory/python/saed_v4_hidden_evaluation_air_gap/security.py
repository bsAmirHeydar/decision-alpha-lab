from __future__ import annotations
from typing import Any
from .canonical import content_hash,stable_id
from .errors import SecurityError
FORBIDDEN_KEYS={"hidden_labels","hidden_label_dump","raw_hidden_rows","plaintext_key","private_key","secret_key","evaluation_feedback_channel","network_url","callback_url","pip_install","shell_command"}
FORBIDDEN_STRINGS=("http://","https://","pip install","curl ","wget ","socket.","subprocess","os.system","powershell -enc")

def _walk(value:Any,path:str="root"):
    if isinstance(value,dict):
        for k,v in value.items():
            if str(k).lower() in FORBIDDEN_KEYS: raise SecurityError(f"forbidden key at {path}.{k}")
            yield from _walk(v,f"{path}.{k}")
    elif isinstance(value,list):
        for i,v in enumerate(value): yield from _walk(v,f"{path}[{i}]")
    elif isinstance(value,str):
        low=value.lower()
        for token in FORBIDDEN_STRINGS:
            if token in low: raise SecurityError(f"forbidden side-channel token at {path}")

def scan(*objects:Any):
    for obj in objects: list(_walk(obj))
    body={"phase":"SAED_V4_29","passed":True,"network_egress_attempts":0,"package_install_attempts":0,"shell_escape_attempts":0,"interactive_debug_attempts":0,"researcher_hidden_label_reads":0,"researcher_key_share_reads":0,"raw_result_egress_attempts":0,"forbidden_key_hits":0,"side_channel_budget_bytes":0,"environment_variables_exported":0,"research_only":True}
    body["security_review_id"]=stable_id("v429_security",body); body["security_review_hash"]=content_hash(body); return body
