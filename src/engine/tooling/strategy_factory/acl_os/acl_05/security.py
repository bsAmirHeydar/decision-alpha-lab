from __future__ import annotations
from pathlib import Path
from .canonical import digest_object

SKIP={"security.py","validate_acl_05.py","run_acl_05_full_qa.py","validate_acl_05_delivery.py"}

def evaluate_security(package_root: Path) -> dict:
    forbidden=("OrderSend"+"(","CTrade","trade.Buy"+"(","trade.Sell"+"(","requests.get"+"(","subprocess.Popen"+"(")
    findings=[]
    for path in sorted(package_root.glob("*.py")):
        if path.name in SKIP: continue
        text=path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in text: findings.append({"path":path.name,"token":token,"reason_code":"ACL05_FORBIDDEN_CAPABILITY_SURFACE"})
    body={"schema_version":"1.0.0","network_access_allowed":False,"live_order_submission_allowed":False,"capital_activation_allowed":False,"secret_access_allowed":False,"filesystem_scope":"DECLARED_INPUTS_AND_OUTPUT_STAGING_ONLY","forbidden_capability_findings":findings,"passed":not findings}
    return {**body,"report_digest":digest_object(body)}
