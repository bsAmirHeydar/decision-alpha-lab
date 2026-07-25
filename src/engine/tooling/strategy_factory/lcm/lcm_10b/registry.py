from __future__ import annotations
from pathlib import Path
from .io import load_json,load_jsonl
class TreatmentPackageRegistry:
    def __init__(self,root:Path):
        self.root=root;self.envelope=load_json(root/"registries/treatment_package_registry.json");self.records=load_jsonl(root/"registries/treatment_package_registry.jsonl");self.by_id={x["treatment_package_id"]:x for x in self.records};self.by_source={x["source_path"]:x for x in self.records}
    def load_package(self,package_id:str)->dict:return load_json(self.root/self.by_id[package_id]["package_path"])
    def resolve_source(self,path:str)->dict|None:
        r=self.by_source.get(path);return self.load_package(r["treatment_package_id"]) if r else None
