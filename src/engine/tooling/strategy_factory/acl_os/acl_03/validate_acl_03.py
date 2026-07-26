from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
import yaml
from ..common import REPO_ROOT
from .policies import POLICY_ROOT,SCHEMA_ROOT

def validate(root:Path=REPO_ROOT)->dict:
    checks=[]
    def add(ok,code,msg,**details): checks.append({"passed":bool(ok),"code":code,"message":msg,"details":details})
    schemas=list(SCHEMA_ROOT.glob("*.schema.json"));add(len(schemas)>=20,"SCHEMA_COUNT",f"{len(schemas)} closed schemas")
    for p in schemas:
        try:
            o=json.loads(p.read_text(encoding="utf-8"));Draft202012Validator.check_schema(o);add(o.get("additionalProperties") is False,"SCHEMA_CLOSED",str(p.relative_to(root)))
        except Exception as e:add(False,"SCHEMA_INVALID",str(e),path=str(p))
    policies=list(POLICY_ROOT.glob("*.yaml"));add(len(policies)>=13,"POLICY_COUNT",f"{len(policies)} policies")
    for p in policies:
        try:add(isinstance(yaml.safe_load(p.read_text(encoding="utf-8")),dict),"POLICY_PARSE",str(p.relative_to(root)))
        except Exception as e:add(False,"POLICY_PARSE",str(e),path=str(p))
    docs=root/"docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_03"; notes=list(docs.glob("*.md"));add(len(notes)>=45,"PHASE_DOCS",f"{len(notes)} phase notes")
    atomic=list((root/"docs/architecture/master/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_03").glob("*.md"));add(len(atomic)>=100,"ATOMIC_DOCS",f"{len(atomic)} atomic notes")
    mql=list((root/"mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL03").glob("*.mqh"));add(len(mql)>=10,"MQL5_STATIC",f"{len(mql)} files")
    forbidden=["OrderSend(","CTrade","PositionOpen(","WebRequest(","FileOpen(","capital_activation_allowed=true","live_order_submission_allowed=true"]
    for p in mql:
        text=p.read_text(encoding="utf-8")
        for token in forbidden:add(token not in text,"MQL5_NON_TRADING",f"{p.name}:{token}")
    module=root/"src/engine/tooling/strategy_factory/acl_os/acl_03"; add((module/"service.py").is_file(),"MODULE_SERVICE","service exists")
    add((root/"src/engine/legacy/acl_os_reference/fixtures/acl_03/valid_context/context_manifest.yaml").is_file(),"VALID_FIXTURE","valid compiler fixture exists")
    return {"passed":all(x["passed"] for x in checks),"checks":checks,"claim_ceiling":"CONTEXT_COMPILATION_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
