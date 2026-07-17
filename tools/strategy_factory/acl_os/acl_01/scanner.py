from __future__ import annotations
from pathlib import Path
import json
from .canonical import digest_file
from .types import ArtifactDescriptor,Reason

class RepositoryScanner:
    def __init__(self,registry,repo_root:Path): self.registry=registry; self.repo_root=repo_root
    def scan(self)->dict:
        findings=[]; seen_paths=set()
        for aid,d in sorted(self.registry.artifacts.items()):
            p=self.repo_root/d.canonical_path; seen_paths.add(d.canonical_path)
            if not p.exists(): findings.append(Reason("REGISTERED_FILE_MISSING","Registered artifact file is missing.",{"artifact_id":aid,"path":d.canonical_path}))
            elif p.is_symlink(): findings.append(Reason("REGISTERED_PATH_SYMLINK","Registered artifact path is a symlink.",{"path":d.canonical_path}))
            elif digest_file(p)!=d.identity.digest: findings.append(Reason("REGISTERED_FILE_DIGEST_DRIFT","Registered artifact content has drifted.",{"artifact_id":aid}))
            findings.extend(self.registry.paths.validate(d))
        # Descriptor sidecars are discoverable and must not silently shadow registry state.
        for p in self.repo_root.rglob("*.artifact.json"):
            if any(part in {".git","__pycache__",".pytest_cache"} for part in p.parts): continue
            rel=p.relative_to(self.repo_root).as_posix()
            try: d=ArtifactDescriptor.from_dict(json.loads(p.read_text(encoding="utf-8")))
            except Exception as exc:
                findings.append(Reason("DESCRIPTOR_SIDECAR_INVALID","Artifact descriptor sidecar is invalid.",{"path":rel,"error":str(exc)})); continue
            registered=self.registry.artifacts.get(d.identity.artifact_id)
            if not registered: findings.append(Reason("UNREGISTERED_ARTIFACT_DESCRIPTOR","Descriptor sidecar names an unregistered artifact.",{"path":rel,"artifact_id":d.identity.artifact_id}))
            elif registered.to_dict()!=d.to_dict(): findings.append(Reason("DESCRIPTOR_REGISTRY_DIVERGENCE","Descriptor sidecar differs from registry record.",{"path":rel}))
        return {"passed":not findings,"findings":[x.to_dict() for x in findings],"registered_artifacts":len(self.registry.artifacts),"registry_digest":self.registry.digest,"live_order_submission_allowed":False,"capital_activation_allowed":False}
