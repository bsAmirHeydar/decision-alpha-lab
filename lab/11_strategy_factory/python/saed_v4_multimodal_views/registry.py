from .authority import assert_safe_boundary
from .errors import RegistryError
class ViewSpecificationRegistry:
    def __init__(self):self._items={}
    def register(self,spec):
        assert_safe_boundary(spec.authority)
        key=(spec.view_name,spec.exact_version);old=self._items.get(key)
        if old and old.semantic_hash!=spec.semantic_hash:raise RegistryError('exact view version rebind')
        if len({x.feature_id for x in spec.features})!=len(spec.features):raise RegistryError('duplicate feature id')
        if not spec.features:raise RegistryError('view requires features')
        self._items[key]=spec;return spec
    def get(self,name,version):
        try:return self._items[(name,version)]
        except KeyError:raise RegistryError('unknown view version')
    def all(self):return tuple(self._items[k] for k in sorted(self._items))
class ViewArtifactRegistry:
    def __init__(self):self._items={}
    def register(self,view):
        key=(view.view_id,view.exact_version);old=self._items.get(key)
        if old and old.view_hash!=view.view_hash:raise RegistryError('view artifact rebind')
        self._items[key]=view;return view
    def all(self):return tuple(self._items[k] for k in sorted(self._items))
