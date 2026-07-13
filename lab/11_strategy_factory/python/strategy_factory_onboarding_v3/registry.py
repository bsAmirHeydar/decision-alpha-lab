from __future__ import annotations
from dataclasses import dataclass
from .contracts import ScaffoldManifest
from .canonical import canonical_sha256
from .errors import OnboardingError
@dataclass
class ContextRegistry:
    manifests:dict[str,ScaffoldManifest]
    def __init__(self):self.manifests={}
    def register(self,manifest:ScaffoldManifest)->str:
        existing=self.manifests.get(manifest.context_id)
        if existing and existing.manifest_hash!=manifest.manifest_hash:raise OnboardingError('static_registry_conflict','same context id has different exact manifest')
        self.manifests[manifest.context_id]=manifest;return self.snapshot_hash
    @property
    def snapshot_hash(self):return canonical_sha256({k:v.manifest_hash for k,v in sorted(self.manifests.items())})
