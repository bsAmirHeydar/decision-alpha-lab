from __future__ import annotations
from .models import ArtifactDescriptor
from .errors import ImmutableConflict
from .canonical import content_hash
class ArtifactCatalog:
    def __init__(self): self._items:dict[tuple[str,str],ArtifactDescriptor]={}
    def register(self,item:ArtifactDescriptor)->ArtifactDescriptor:
        key=(item.artifact_id,item.exact_version)
        if key in self._items:
            if self._items[key].descriptor_hash!=item.descriptor_hash: raise ImmutableConflict('artifact exact-version conflict')
            return self._items[key]
        self._items[key]=item; return item
    def get(self,artifact_id:str,exact_version:str)->ArtifactDescriptor: return self._items[(artifact_id,exact_version)]
    def all(self): return tuple(self._items[k] for k in sorted(self._items))
    def catalog_hash(self): return content_hash([x.semantic_payload() for x in self.all()])
