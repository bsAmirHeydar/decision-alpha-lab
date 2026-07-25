from __future__ import annotations
from pathlib import Path, PurePosixPath
from .errors import ContractError
from .types import ArtifactDescriptor, ArtifactMutability, Reason


def _safe_rel(path:str)->PurePosixPath:
    p=PurePosixPath(path)
    if p.is_absolute() or ".." in p.parts or not p.parts: raise ContractError(f"unsafe repository path: {path}")
    if any(part in {".",""} for part in p.parts): raise ContractError(f"non-canonical repository path: {path}")
    return p

class PathPolicy:
    def __init__(self,policies):
        self.zones=policies.documents["repository_zones"]["zones"]
        self.templates=policies.documents["path_templates"]["templates"]
        self.generated=policies.documents["generated_content_policy"]

    def classify(self,path:str)->str|None:
        p=_safe_rel(path).as_posix()
        matches=[]
        for zone,spec in self.zones.items():
            for root in spec.get("roots",[]):
                root=root.rstrip("/")
                if p==root or p.startswith(root+"/"): matches.append((len(root),zone))
        return max(matches)[1] if matches else None

    def canonical_path(self,descriptor:ArtifactDescriptor,filename:str)->str:
        if "/" in filename or filename in {".",".."}: raise ContractError("filename must be a single safe component")
        tmpl=self.templates.get(descriptor.identity.kind,self.templates["default"])
        values={**descriptor.identity.to_dict(),"zone":descriptor.zone,"filename":filename}
        path=tmpl.format(**values)
        _safe_rel(path)
        return path

    def validate(self,d:ArtifactDescriptor)->list[Reason]:
        reasons=[]
        zone=self.classify(d.canonical_path)
        if zone is None: reasons.append(Reason("PATH_OUTSIDE_REGISTERED_ZONE","Artifact path is outside all registered repository zones.",{"path":d.canonical_path}))
        elif zone!=d.zone: reasons.append(Reason("PATH_ZONE_MISMATCH","Declared zone does not match path classification.",{"declared":d.zone,"classified":zone}))
        spec=self.zones.get(d.zone)
        if not spec: reasons.append(Reason("UNKNOWN_REPOSITORY_ZONE","Declared repository zone is unknown.",{"zone":d.zone})); return reasons
        allowed=set(spec.get("allowed_mutability",[]))
        if d.mutability.value not in allowed: reasons.append(Reason("MUTABILITY_ZONE_VIOLATION","Artifact mutability is forbidden in this zone.",{"mutability":d.mutability.value,"zone":d.zone}))
        if d.mutability==ArtifactMutability.GENERATED:
            header=d.metadata.get("generation")
            required=set(self.generated["required_metadata"])
            if not isinstance(header,dict) or not required<=set(header): reasons.append(Reason("GENERATED_PROVENANCE_MISSING","Generated artifact lacks required generator and source provenance.",{"required":sorted(required)}))
        if d.mutability==ArtifactMutability.AUTHORED and d.zone in set(self.generated.get("generated_only_zones",[])):
            reasons.append(Reason("AUTHORED_FILE_IN_GENERATED_ZONE","Authored artifact cannot be placed in generated-only zone.",{}))
        return reasons
