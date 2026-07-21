from __future__ import annotations
from pathlib import Path
from .io import load_json,load_jsonl
class LCM10BFactoryReference:
    def __init__(self,root:Path):
        self.root=root;self.bindings=load_jsonl(root/"bindings/setup_treatment_package_binding_registry.jsonl");self.by_setup={x["setup_id"]:x for x in self.bindings}
    def resolve(self,setup_id:str)->dict:
        b=self.by_setup[setup_id]
        if b["binding_status"]!="BOUND_REFERENCE":return {"resolved":False,"blocker_ids":b["blocker_ids"],"execution_authorized":False}
        return {"resolved":True,"treatment_package_ids":b["treatment_package_ids"],"execution_authorized":False,"claim_ceiling":b["claim_ceiling"]}
