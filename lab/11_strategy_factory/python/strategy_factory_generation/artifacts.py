from __future__ import annotations
from dataclasses import dataclass,replace
@dataclass(frozen=True,slots=True)
class ArtifactEntry:
    artifact_id:str;relative_path:str;content_type:str;schema_key:str;sealed:bool=False;record_count:int=0;byte_count:int=0;final_hash:str=''
class ArtifactCatalog:
    def __init__(self):self._entries={};self._paths=set()
    def add(self,e:ArtifactEntry):
        if '..' in e.relative_path:raise ValueError('path traversal')
        if e.artifact_id in self._entries or e.relative_path in self._paths:raise ValueError('duplicate artifact')
        self._entries[e.artifact_id]=e;self._paths.add(e.relative_path)
    def seal(self,artifact_id:str,records:int,bytes_:int,final_hash:str):
        e=self._entries[artifact_id]
        if e.sealed:raise ValueError('already sealed')
        self._entries[artifact_id]=replace(e,sealed=True,record_count=records,byte_count=bytes_,final_hash=final_hash)
    def get(self,artifact_id):return self._entries[artifact_id]
    def __len__(self):return len(self._entries)
