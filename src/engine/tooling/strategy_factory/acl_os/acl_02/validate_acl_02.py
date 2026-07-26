from __future__ import annotations
import json,re
from pathlib import Path
from jsonschema import Draft202012Validator
import yaml
from ..common import REPO_ROOT
from .policies import POLICY_ROOT,SCHEMA_ROOT

def validate(root:Path=REPO_ROOT)->dict:
    checks=[]
    def add(ok,code,msg,**d):checks.append({"passed":bool(ok),"code":code,"message":msg,"details":d})
    schemas=list(SCHEMA_ROOT.glob("*.schema.json"));add(len(schemas)>=17,"SCHEMA_COUNT",f"{len(schemas)} closed schemas")
    for p in schemas:
        try:o=json.loads(p.read_text());Draft202012Validator.check_schema(o);add(o.get("additionalProperties") is False,"SCHEMA_CLOSED",str(p.relative_to(root)))
        except Exception as e:add(False,"SCHEMA_INVALID",str(e),path=str(p))
    policies=list(POLICY_ROOT.glob("*.yaml"));add(len(policies)>=10,"POLICY_COUNT",f"{len(policies)} policies")
    for p in policies:
        try:add(isinstance(yaml.safe_load(p.read_text()),dict),"POLICY_PARSE",str(p.relative_to(root)))
        except Exception as e:add(False,"POLICY_PARSE",str(e),path=str(p))
    template=root/"contexts/legacy/strategy_factory/authored/_acl_02_template"; required=["context_manifest.yaml","owners.yaml","doctrine/context_doctrine.md","contracts/scope.yaml","contracts/ontology.yaml","contracts/causal_clock.yaml","contracts/data_contract.yaml","contracts/state_machine.yaml","contracts/occurrence_contract.yaml","contracts/reference_contract.yaml","contracts/feature_views.yaml","contracts/treatment_envelope.yaml","contracts/acceptance_gates.yaml","security/security_profile.yaml","fixtures/example_catalog.yaml","governance/amendment_policy.yaml"]
    for rel in required:add((template/rel).is_file(),"TEMPLATE_REQUIRED",rel)
    docs=root/"docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_02";notes=list(docs.glob("*.md"));add(len(notes)>=40,"PHASE_DOCS",f"{len(notes)} phase notes")
    atomic=list((root/"docs/architecture/master/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_02").glob("*.md"));add(len(atomic)>=80,"ATOMIC_DOCS",f"{len(atomic)} atomic notes")
    mql=list((root/"mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL02").glob("*.mqh"));add(len(mql)>=8,"MQL5_STATIC",f"{len(mql)} files")
    forbidden=["OrderSend(","CTrade","PositionOpen(","capital_activation_allowed=true","live_order_submission_allowed=true"]
    for p in mql:
        text=p.read_text()
        for token in forbidden:add(token not in text,"MQL5_NON_TRADING",f"{p.name}:{token}")
    return {"passed":all(x["passed"] for x in checks),"checks":checks,"claim_ceiling":"SEMANTIC_INTAKE_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
