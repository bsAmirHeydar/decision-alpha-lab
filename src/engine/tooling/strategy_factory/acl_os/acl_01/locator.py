from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
from .canonical import digest_file
from .identity import artifact_base
from .semver import Version,satisfies
from .types import LocatorResult,Reason,ResolutionStatus,RegistryStatus

class ArtifactLocator:
    def __init__(self,registry,repo_root:Path): self.registry=registry; self.repo_root=repo_root
    def resolve(self,ref:str,version_constraint:str|None=None,verify_file:bool=True,now:datetime|None=None)->LocatorResult:
        now=(now or datetime.now(timezone.utc)).astimezone(timezone.utc); reasons=[]; requested=ref
        exact,alias_reasons=self.registry.resolve_alias(ref)
        descriptor=None
        if exact:
            descriptor=self.registry.artifacts[exact]
            if version_constraint and not satisfies(descriptor.identity.version,version_constraint):
                descriptor=None; reasons.append(Reason("VERSION_CONSTRAINT_UNSATISFIED","Resolved exact artifact does not satisfy requested range.",{}))
        else:
            # Base-ID resolution requires an explicit version range. This prevents
            # a mutable, implicit "latest" dependency from entering the graph.
            if ref.startswith("al://") and "@" not in ref and not version_constraint:
                reasons.append(Reason("BASE_ID_VERSION_CONSTRAINT_REQUIRED","Base artifact IDs require an explicit semantic-version constraint.",{"ref":ref}))
                candidates=[]
            else:
                candidates=[d for d in self.registry.artifacts.values() if d.identity.base_id==ref and (not version_constraint or satisfies(d.identity.version,version_constraint)) and d.status==RegistryStatus.ACTIVE]
            if candidates:
                candidates.sort(key=lambda d:Version.parse(d.identity.version),reverse=True); descriptor=candidates[0]
            else: reasons.extend(alias_reasons)
        if descriptor and descriptor.status in {RegistryStatus.QUARANTINED,RegistryStatus.TOMBSTONED}:
            reasons.append(Reason("ARTIFACT_NOT_RESOLVABLE_STATUS","Artifact status prevents resolution.",{"status":descriptor.status.value})); descriptor=None
        verified=False
        if descriptor and verify_file:
            path=self.repo_root/descriptor.canonical_path
            try:
                real=path.resolve(strict=True); root=self.repo_root.resolve(strict=True)
                if root not in real.parents and real!=root: reasons.append(Reason("LOCATOR_PATH_ESCAPE","Resolved path escapes repository root.",{})); descriptor=None
                elif path.is_symlink(): reasons.append(Reason("LOCATOR_SYMLINK_DENIED","Canonical artifact path may not be a symlink.",{})); descriptor=None
                else:
                    got=digest_file(path)
                    if got!=descriptor.identity.digest: reasons.append(Reason("ARTIFACT_DIGEST_MISMATCH","Artifact bytes do not match registered digest.",{"expected":descriptor.identity.digest,"actual":got})); descriptor=None
                    else: verified=True
            except FileNotFoundError:
                reasons.append(Reason("ARTIFACT_FILE_MISSING","Registered artifact file is missing.",{"path":descriptor.canonical_path})); descriptor=None
        status=ResolutionStatus.RESOLVED if descriptor and not reasons else (ResolutionStatus.INTEGRITY_FAILURE if any(r.code in {"ARTIFACT_DIGEST_MISMATCH","LOCATOR_PATH_ESCAPE","LOCATOR_SYMLINK_DENIED"} for r in reasons) else ResolutionStatus.NOT_FOUND)
        return LocatorResult(status,requested,descriptor,tuple(reasons),now,self.registry.digest,verified,False,False)
