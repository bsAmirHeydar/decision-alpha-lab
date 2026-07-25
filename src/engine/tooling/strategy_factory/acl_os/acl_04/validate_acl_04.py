from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
import yaml
from ..common import REPO_ROOT
from .policies import POLICY_ROOT, SCHEMA_ROOT


def validate(root: Path=REPO_ROOT) -> dict:
    checks=[]
    def add(ok,code,message,**details): checks.append({"passed":bool(ok),"code":code,"message":message,"details":details})
    schemas=sorted(SCHEMA_ROOT.glob("*.schema.json")); add(len(schemas)>=20,"ACL04_SCHEMA_COUNT",f"{len(schemas)} schemas")
    for path in schemas:
        try:
            obj=json.loads(path.read_text(encoding="utf-8")); Draft202012Validator.check_schema(obj); add(obj.get("additionalProperties") is False,"ACL04_SCHEMA_CLOSED",str(path.relative_to(root)))
        except Exception as exc: add(False,"ACL04_SCHEMA_INVALID",str(exc),path=str(path))
    policies=sorted(POLICY_ROOT.glob("*.yaml")); add(len(policies)>=14,"ACL04_POLICY_COUNT",f"{len(policies)} policies")
    for path in policies:
        try: add(isinstance(yaml.safe_load(path.read_text(encoding="utf-8")),dict),"ACL04_POLICY_PARSE",str(path.relative_to(root)))
        except Exception as exc: add(False,"ACL04_POLICY_PARSE",str(exc),path=str(path))
    phase_docs=list((root/"docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_04").glob("*.md")); add(len(phase_docs)>=45,"ACL04_PHASE_DOCS",f"{len(phase_docs)} notes")
    atomic=list((root/"docs/alpha_lab_master_architecture/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_04").glob("*.md")); add(len(atomic)>=100,"ACL04_ATOMIC_DOCS",f"{len(atomic)} notes")
    mql=list((root/"mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL04").glob("*.mqh")); add(len(mql)>=12,"ACL04_MQL5_STATIC",f"{len(mql)} files")
    forbidden=["OrderSend(","CTrade","PositionOpen(","WebRequest(","capital_activation_allowed=true","live_order_submission_allowed=true"]
    for path in mql:
        text=path.read_text(encoding="utf-8")
        for token in forbidden: add(token not in text,"ACL04_MQL5_NON_TRADING",f"{path.name}:{token}")
    module=root/"src/engine/tooling/strategy_factory/acl_os/acl_04"; add((module/"service.py").is_file(),"ACL04_SERVICE_EXISTS","service exists")
    fixture=root/"src/engine/legacy/acl_os_reference/fixtures/acl_04"; add((fixture/"human_setup.yaml").is_file(),"ACL04_FIXTURE_EXISTS","fixture exists")
    return {"passed":all(x["passed"] for x in checks),"checks":checks,"claim_ceiling":"SETUP_DEFINITION_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
