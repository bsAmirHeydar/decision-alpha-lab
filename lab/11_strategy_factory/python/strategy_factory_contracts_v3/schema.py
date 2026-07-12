"""Exact schema identities and an immutable-by-convention registry."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Mapping
from .errors import SchemaError
from .hashing import canonical_sha256
from .validation import require_safe_identifier, require_unique

@dataclass(frozen=True, slots=True, order=True)
class SemanticVersion:
    major:int
    minor:int
    patch:int

    def __post_init__(self) -> None:
        if any(not isinstance(v,int) or isinstance(v,bool) or v<0 for v in (self.major,self.minor,self.patch)):
            raise SchemaError("invalid_semantic_version", "semantic version components must be non-negative integers")

    @classmethod
    def parse(cls,value:str) -> "SemanticVersion":
        try:
            parts=tuple(int(part) for part in value.split("."))
        except ValueError as exc:
            raise SchemaError("invalid_semantic_version", "version contains non-integer components", {"value":value}) from exc
        if len(parts)!=3:
            raise SchemaError("invalid_semantic_version", "version must contain major.minor.patch", {"value":value})
        return cls(*parts)

    def __str__(self) -> str: return f"{self.major}.{self.minor}.{self.patch}"

@dataclass(frozen=True, slots=True)
class SchemaId:
    namespace:str
    name:str
    version:SemanticVersion

    def __post_init__(self) -> None:
        require_safe_identifier(self.namespace,"schema.namespace")
        require_safe_identifier(self.name,"schema.name")

    @property
    def family_key(self) -> str: return f"{self.namespace}/{self.name}"
    @property
    def exact_key(self) -> str: return f"{self.family_key}@{self.version}"

@dataclass(frozen=True, slots=True)
class SchemaDescriptor:
    schema_id:SchemaId
    semantic_owner:str
    required_fields:tuple[str,...]
    optional_fields:tuple[str,...]=()
    enum_domains:Mapping[str,tuple[str,...]] | None=None
    description:str=""

    def __post_init__(self) -> None:
        require_safe_identifier(self.semantic_owner,"semantic_owner")
        require_unique(self.required_fields,"required_fields")
        require_unique(self.optional_fields,"optional_fields")
        overlap=set(self.required_fields).intersection(self.optional_fields)
        if overlap: raise SchemaError("field_role_overlap","fields cannot be both required and optional",{"fields":sorted(overlap)})

    @property
    def semantic_hash(self) -> str:
        return canonical_sha256({
            "enum_domains":dict(self.enum_domains or {}),
            "optional_fields":list(self.optional_fields),
            "required_fields":list(self.required_fields),
            "schema_id":self.schema_id.exact_key,
            "semantic_owner":self.semantic_owner,
        })

class SchemaRegistry:
    def __init__(self, descriptors: Iterable[SchemaDescriptor]=()) -> None:
        self._by_exact:dict[str,SchemaDescriptor]={}
        for descriptor in descriptors: self.register(descriptor)

    def register(self, descriptor:SchemaDescriptor) -> None:
        key=descriptor.schema_id.exact_key
        if key in self._by_exact:
            existing=self._by_exact[key]
            if existing.semantic_hash != descriptor.semantic_hash:
                raise SchemaError("schema_redefinition", "exact schema key was redefined with different semantics", {"schema":key})
            return
        self._by_exact[key]=descriptor

    def resolve_exact(self, schema_id:SchemaId | str) -> SchemaDescriptor:
        key=schema_id if isinstance(schema_id,str) else schema_id.exact_key
        try: return self._by_exact[key]
        except KeyError as exc: raise SchemaError("unknown_exact_schema", "schema is not registered exactly", {"schema":key}) from exc

    def require_supported_major(self, namespace:str,name:str,major:int) -> None:
        candidates=[d for d in self._by_exact.values() if d.schema_id.namespace==namespace and d.schema_id.name==name and d.schema_id.version.major==major]
        if not candidates: raise SchemaError("unknown_schema_major","schema major is unsupported",{"family":f"{namespace}/{name}","major":major})

    def manifest(self) -> list[dict[str,str]]:
        return [{"exact_key":key,"semantic_hash":self._by_exact[key].semantic_hash} for key in sorted(self._by_exact)]
