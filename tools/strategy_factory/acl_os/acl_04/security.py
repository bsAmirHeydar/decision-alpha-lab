from __future__ import annotations
from pathlib import Path
from typing import Any
from .canonical import digest_object

FORBIDDEN_TOKENS = ["eval(", "exec(", "subprocess", "socket", "requests.", "urllib", "OrderSend(", "CTrade", "PositionOpen("]


def evaluate_security(package_root: Path) -> dict[str, Any]:
    findings=[]
    excluded={"security.py","run_acl_04_full_qa.py","validate_acl_04.py","validate_acl_04_delivery.py"}
    for path in sorted(package_root.glob("*.py")):
        if path.name in excluded:
            continue
        text=path.read_text(encoding="utf-8")
        for token in FORBIDDEN_TOKENS:
            if token in text:
                findings.append({"code":"ACL04_FORBIDDEN_CAPABILITY_TOKEN","path":str(path),"token":token})
    body={
        "schema_version":"1.0.0",
        "passed":not findings,
        "findings":findings,
        "network_egress_allowed":False,
        "secret_access_allowed":False,
        "live_order_submission_allowed":False,
        "capital_activation_allowed":False,
        "dynamic_evaluation_allowed":False,
    }
    return {**body,"report_digest":digest_object(body)}
