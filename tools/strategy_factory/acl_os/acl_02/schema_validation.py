from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .policies import SCHEMA_ROOT
from .types import Finding,Severity

SECTION_SCHEMA={
"manifest":"context_manifest","owners":"owner_assignment","scope":"scope_contract","ontology":"ontology_contract","causal_clock":"causal_clock_contract","data":"data_contract","state_machine":"state_machine_contract","occurrence":"occurrence_contract","references":"reference_contract","feature_views":"feature_view_contract","treatment_envelope":"treatment_envelope","acceptance_gates":"acceptance_gate_contract","security_profile":"security_profile","examples":"example_catalog","amendments":"amendment_policy","glossary":"glossary_contract"}

def validate_schemas(package:dict,paths:dict)->list[Finding]:
    findings=[]
    for key,name in SECTION_SCHEMA.items():
        obj=package.get(key); schema_path=SCHEMA_ROOT/f"{name}.schema.json"
        if not schema_path.is_file():
            findings.append(Finding("ACL02_SCHEMA_NOT_REGISTERED",Severity.BLOCKER,paths.get(key,key),f"schema missing for {key}","register the closed schema")); continue
        schema=json.loads(schema_path.read_text(encoding="utf-8"))
        errors=sorted(Draft202012Validator(schema).iter_errors(obj),key=lambda e:list(e.absolute_path))
        for e in errors:
            suffix="/".join(str(x) for x in e.absolute_path)
            findings.append(Finding("ACL02_SCHEMA_VALIDATION_FAILED",Severity.BLOCKER,f"{paths.get(key,key)}#{suffix}",e.message,"correct the authored contract to the registered schema"))
    return findings
