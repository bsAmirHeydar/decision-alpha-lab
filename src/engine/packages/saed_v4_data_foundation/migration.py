from __future__ import annotations
from typing import Callable,Mapping,Any
from .canonical import content_hash
from .errors import IntegrityViolation
class MigrationRegistry:
    def __init__(self): self._items={}
    def register(self,schema_name:str,from_version:str,to_version:str,transform:Callable[[Mapping[str,Any]],Mapping[str,Any]],transform_source_hash:str): self._items[(schema_name,from_version,to_version)]=(transform,transform_source_hash)
    def migrate(self,schema_name:str,from_version:str,to_version:str,document:Mapping[str,Any],expected_output_hash:str|None=None):
        transform,source_hash=self._items[(schema_name,from_version,to_version)]; out=dict(transform(document)); digest=content_hash(out)
        if expected_output_hash and digest!=expected_output_hash: raise IntegrityViolation('migration output hash mismatch')
        return out,source_hash,digest
