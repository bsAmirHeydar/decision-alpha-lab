from __future__ import annotations
from pathlib import Path
from typing import Any
from .errors import PackageLoadError
from .io import load_structured,load_yaml

def _parse_doctrine_markdown(text: str) -> dict:
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip().lower().replace(" — non-authoritative", "").replace(" ", "_").replace("-", "_")
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return {"raw_markdown": text, **sections}

REQUIRED_CONTRACT_KEYS=("doctrine","glossary","scope","ontology","causal_clock","data","state_machine","occurrence","references","feature_views","treatment_envelope","acceptance_gates","security_profile","examples","amendments")

class ContextPackageLoader:
    def __init__(self,root:Path): self.root=root.resolve()
    def load(self)->dict[str,Any]:
        manifest_path=self.root/"context_manifest.yaml"
        if not manifest_path.is_file(): raise PackageLoadError(f"missing manifest: {manifest_path}")
        manifest=load_yaml(manifest_path); contracts=manifest.get("contracts")
        if not isinstance(contracts,dict): raise PackageLoadError("manifest contracts must be a mapping")
        package={"manifest":manifest,"_paths":{"manifest":"context_manifest.yaml"}}
        for key in REQUIRED_CONTRACT_KEYS:
            rel=contracts.get(key)
            if not isinstance(rel,str) or not rel: raise PackageLoadError(f"missing contract path: {key}")
            path=(self.root/rel).resolve()
            if self.root not in path.parents: raise PackageLoadError(f"path escapes context root: {rel}")
            if not path.is_file(): raise PackageLoadError(f"missing contract file: {rel}")
            value=load_structured(path)
            if key=="doctrine" and isinstance(value,str): value=_parse_doctrine_markdown(value)
            package[key]=value; package["_paths"][key]=rel
        owners_rel=manifest.get("owners_file","owners.yaml")
        owners=(self.root/owners_rel).resolve()
        if self.root not in owners.parents or not owners.is_file(): raise PackageLoadError("invalid owners_file")
        package["owners"]=load_yaml(owners); package["_paths"]["owners"]=owners_rel
        return package
