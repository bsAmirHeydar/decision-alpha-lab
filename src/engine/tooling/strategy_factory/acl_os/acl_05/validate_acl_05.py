from __future__ import annotations
import json, py_compile
from pathlib import Path
from jsonschema import Draft202012Validator
from .policies import PACKAGE_ROOT, POLICY_ROOT, SCHEMA_ROOT

SKIP_SCAN={"validate_acl_05.py","security.py","run_acl_05_full_qa.py","validate_acl_05_delivery.py"}

def run() -> dict:
    checks=[]
    def add(name,passed,detail=""): checks.append({"name":name,"passed":bool(passed),"detail":detail})
    py=list(PACKAGE_ROOT.glob("*.py")); schemas=list(SCHEMA_ROOT.glob("*.schema.json")); policies=list(POLICY_ROOT.glob("*.json"))
    compile_errors=[]
    for p in py:
        try: py_compile.compile(str(p),doraise=True)
        except Exception as exc: compile_errors.append(f"{p.name}:{exc}")
    add("python_compile",not compile_errors,";".join(compile_errors))
    schema_errors=[]
    for p in schemas:
        try: Draft202012Validator.check_schema(json.loads(p.read_text(encoding="utf-8")))
        except Exception as exc: schema_errors.append(f"{p.name}:{exc}")
    add("closed_schema_registry",len(schemas)>=25 and not schema_errors,f"count={len(schemas)};"+";".join(schema_errors))
    policy_errors=[]
    for p in policies:
        try: json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc: policy_errors.append(f"{p.name}:{exc}")
    add("policy_registry",len(policies)>=20 and not policy_errors,f"count={len(policies)};"+";".join(policy_errors))
    forbidden=("OrderSend"+"(","trade.Buy"+"(","trade.Sell"+"(","requests.get"+"(")
    findings=[]
    for p in py:
        if p.name in SKIP_SCAN: continue
        text=p.read_text(encoding="utf-8")
        findings.extend(f"{p.name}:{t}" for t in forbidden if t in text)
    add("forbidden_capability_scan",not findings,";".join(findings))
    result={"phase":"ACL-05","checks":checks,"passed":all(c["passed"] for c in checks)}
    print(json.dumps(result,indent=2,sort_keys=True)); return result

if __name__=="__main__": raise SystemExit(0 if run()["passed"] else 2)
