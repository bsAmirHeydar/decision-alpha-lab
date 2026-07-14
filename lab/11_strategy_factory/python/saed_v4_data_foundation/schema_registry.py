from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping
from jsonschema import Draft202012Validator
from .canonical import content_hash
from .errors import ImmutableConflict,ContractError
@dataclass(frozen=True)
class RegisteredSchema:
    name:str; version:str; schema:Mapping[str,Any]; schema_hash:str
class SchemaRegistry:
    def __init__(self): self._schemas:dict[tuple[str,str],RegisteredSchema]={}; self._migrations:dict[tuple[str,str,str],str]={}
    def register(self,name:str,version:str,schema:Mapping[str,Any])->RegisteredSchema:
        Draft202012Validator.check_schema(schema)
        if schema.get('additionalProperties') is not False: raise ContractError('sovereign schemas must be closed')
        key=(name,version); digest=content_hash(schema)
        if key in self._schemas:
            if self._schemas[key].schema_hash!=digest: raise ImmutableConflict('schema version already exists with different content')
            return self._schemas[key]
        r=RegisteredSchema(name,version,dict(schema),digest); self._schemas[key]=r; return r
    def get(self,name:str,version:str)->RegisteredSchema: return self._schemas[(name,version)]
    def validate(self,name:str,version:str,document:Any)->None:
        errors=sorted(Draft202012Validator(self.get(name,version).schema).iter_errors(document),key=lambda e:list(e.absolute_path))
        if errors: raise ContractError('; '.join(e.message for e in errors[:20]))
    def declare_migration(self,name:str,from_version:str,to_version:str,transform_hash:str)->None:
        self.get(name,from_version); self.get(name,to_version); self._migrations[(name,from_version,to_version)]=transform_hash
    def migration_hash(self,name:str,from_version:str,to_version:str)->str|None: return self._migrations.get((name,from_version,to_version))
    def registry_hash(self)->str:
        return content_hash([{'name':x.name,'version':x.version,'schema_hash':x.schema_hash} for x in sorted(self._schemas.values(),key=lambda s:(s.name,s.version))])
