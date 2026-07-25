from __future__ import annotations
from .authority import assert_safe_boundary
from .errors import RegistryError
class EventStreamRegistry:
    def __init__(self):self._items={}
    def register(self,manifest):
        assert_safe_boundary(manifest.authority);key=(manifest.stream_id,manifest.exact_version)
        old=self._items.get(key)
        if old and old.semantic_hash!=manifest.semantic_hash:raise RegistryError('exact stream version rebind')
        self._items[key]=manifest;return manifest
    def get(self,stream_id,version):
        try:return self._items[(stream_id,version)]
        except KeyError:raise RegistryError('unknown stream version')
    def all(self):return tuple(self._items[k] for k in sorted(self._items))
class ProjectionRegistry:
    def __init__(self):self._items={}
    def register(self,definition):
        key=(definition.projection_name,definition.exact_version);old=self._items.get(key)
        if old and old.semantic_hash!=definition.semantic_hash:raise RegistryError('exact projection version rebind')
        if len({f.field_id for f in definition.fields})!=len(definition.fields):raise RegistryError('duplicate projection field')
        self._items[key]=definition;return definition
    def get(self,name,version):return self._items[(name,version)]
