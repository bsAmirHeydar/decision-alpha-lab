from __future__ import annotations
import json,re
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from ..common import REPO_ROOT
from .policies import PolicyBundle

SCHEMA_ROOT=REPO_ROOT/"registry"/"history"/"acl"/"acl_01"/"schemas"/"v1"
DOC_ROOT=REPO_ROOT/"docs"/"alpha_lab_master_architecture"/"context_lifecycle_os"
MQL5_ROOT=REPO_ROOT/"lab"/"11_strategy_factory"/"mql5"/"Include"/"AlphaLab"/"ACL_OS"/"ACL01"

def validate(root:Path=REPO_ROOT)->dict:
    errors=[]; counts={}
    try: bundle=PolicyBundle.load(root/"registry"/"acl_os"/"acl_01"/"policies"/"v1")
    except Exception as exc: errors.append(f"policy bundle: {exc}"); bundle=None
    schemas=list((root/"registry"/"acl_os"/"acl_01"/"schemas"/"v1").glob("*.schema.json")); counts["closed_schemas"]=len(schemas)
    ids=set()
    for p in schemas:
        try:
            obj=json.loads(p.read_text(encoding="utf-8")); Draft202012Validator.check_schema(obj)
            if obj.get("additionalProperties") is not False: errors.append(f"schema not closed: {p}")
            if not obj.get("$id") or obj["$id"] in ids: errors.append(f"schema id invalid/duplicate: {p}")
            ids.add(obj.get("$id"))
        except Exception as exc: errors.append(f"schema {p}: {exc}")
    policies=list((root/"registry"/"acl_os"/"acl_01"/"policies"/"v1").glob("*.yaml")); counts["policy_documents"]=len(policies)
    for p in policies:
        try:
            obj=yaml.safe_load(p.read_text(encoding="utf-8"));
            if not isinstance(obj,dict): errors.append(f"policy not object: {p}")
        except Exception as exc: errors.append(f"policy {p}: {exc}")
    phase=list((root/"docs"/"alpha_lab_master_architecture"/"context_lifecycle_os"/"12_PHASE_DELIVERIES"/"ACL_01").glob("*.md")); atom=list((root/"docs"/"alpha_lab_master_architecture"/"context_lifecycle_os"/"13_ATOMIC_CONCEPTS"/"ACL_01").glob("*.md")); counts["phase_delivery_notes"]=len(phase); counts["atomic_concepts"]=len(atom)
    if len(phase)<30: errors.append("phase delivery documentation below minimum 30")
    if len(atom)<60: errors.append("atomic concept documentation below minimum 60")
    # Local wikilink closure for phase namespace.
    names={p.stem for p in DOC_ROOT.rglob("*.md")}
    link_re=re.compile(r"\[\[([^]|#]+)")
    for p in phase+atom:
        for target in link_re.findall(p.read_text(encoding="utf-8")):
            if target not in names: errors.append(f"broken wikilink {target} in {p}")
    mql=list((root/"lab"/"11_strategy_factory"/"mql5"/"Include"/"AlphaLab"/"ACL_OS"/"ACL01").glob("*.mqh")); counts["mql5_static_files"]=len(mql)
    forbidden=("OrderSend(","CTrade","trade.Buy","trade.Sell","PositionOpen","WebRequest(","Socket")
    for p in mql:
        txt=p.read_text(encoding="utf-8")
        for token in forbidden:
            if token in txt: errors.append(f"forbidden MQL5 token {token} in {p}")
        if "ACL01_LIVE_ORDER_SUBMISSION_ALLOWED false" not in txt and p.name=="ACL01AuthorityEnvelope.mqh": errors.append("MQL5 authority envelope missing hard false")
    # Policy closure.
    if bundle:
        kinds=set(bundle.documents["artifact_kinds"]["kinds"]); templates=set(bundle.documents["path_templates"]["templates"])
        if not kinds<=templates|{"default"}: errors.append("artifact kind missing path template")
        zones=set(bundle.documents["repository_zones"]["zones"])
        for k,spec in bundle.documents["artifact_kinds"]["kinds"].items():
            if spec["default_zone"] not in zones: errors.append(f"kind {k} references unknown zone")
        ranks=bundle.documents["dependency_policy"]["layer_ranks"]
        for k,spec in bundle.documents["artifact_kinds"]["kinds"].items():
            if spec["layer"] not in ranks: errors.append(f"kind {k} references unknown layer")
    return {"passed":not errors,"errors":errors,"counts":counts,"claim_ceiling":"REFERENCE_REPOSITORY_CONTROL_PLANE","live_order_submission_allowed":False,"capital_activation_allowed":False}

if __name__=="__main__": print(json.dumps(validate(),indent=2,sort_keys=True))
