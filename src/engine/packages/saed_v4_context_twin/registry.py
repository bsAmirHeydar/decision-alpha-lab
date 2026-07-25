from __future__ import annotations
from .models import ContextTwinManifest
from .errors import RegistryError
class TwinRegistry:
    def __init__(self):self._items={}
    def register(self,m:ContextTwinManifest):
        key=(m.twin_id,m.exact_version);old=self._items.get(key)
        if old and old.semantic_hash!=m.semantic_hash:raise RegistryError('exact version rebind')
        self._items[key]=m;return m.semantic_hash
    def get(self,twin_id,exact_version):
        try:return self._items[(twin_id,exact_version)]
        except KeyError:raise RegistryError('unknown twin version')
    def versions(self,twin_id):return tuple(sorted(v for (i,v) in self._items if i==twin_id))
