from __future__ import annotations
from pathlib import Path
from .compatibility import CompatibilityRequirement
from .locator import ArtifactLocator
from .policies import PolicyBundle
from .registry import RepositoryRegistry
from .scanner import RepositoryScanner
from .canonical import digest_file
from .types import Reason
from ..common import REPO_ROOT

class ACL01RepositoryControlPlane:
    def __init__(self,repo_root:Path=REPO_ROOT,policies:PolicyBundle|None=None,registry:RepositoryRegistry|None=None):
        self.repo_root=repo_root; self.policies=policies or PolicyBundle.load(); self.registry=registry or RepositoryRegistry(self.policies); self.locator=ArtifactLocator(self.registry,repo_root); self.scanner=RepositoryScanner(self.registry,repo_root)

    def register_artifact(self,descriptor,permit):
        path=self.repo_root/descriptor.canonical_path
        reasons=[]
        if not path.is_file(): reasons.append(Reason("ARTIFACT_FILE_MISSING","Artifact bytes must exist before registration.",{"path":descriptor.canonical_path}))
        elif path.is_symlink(): reasons.append(Reason("LOCATOR_SYMLINK_DENIED","Artifact registration denies symlink paths.",{"path":descriptor.canonical_path}))
        elif digest_file(path)!=descriptor.identity.digest: reasons.append(Reason("ARTIFACT_DIGEST_MISMATCH","Artifact bytes do not match descriptor digest.",{}))
        if reasons:return reasons
        return self.registry.register_artifact(descriptor,permit)

    def resolve(self,ref:str,version_constraint:str|None=None,verify_file:bool=True): return self.locator.resolve(ref,version_constraint,verify_file)
    def scan(self): return self.scanner.scan()
    def validate(self):
        reasons=self.registry.validate_graphs()
        return {"passed":not reasons,"reasons":[x.to_dict() for x in reasons],"registry_digest":self.registry.digest,"revision":self.registry.revision,"live_order_submission_allowed":False,"capital_activation_allowed":False}
    def compatible_provider(self,requirement:CompatibilityRequirement): return self.registry.compat.resolve(requirement,self.registry.artifacts)
