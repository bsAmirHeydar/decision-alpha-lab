from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from .canonical import digest_bytes, digest_object, stable_id
from .errors import BudgetError, StoreError

class ContentAddressedStore:
    def __init__(self,root: Path,max_objects: int,max_bytes: int):
        self.root=root; self.max_objects=max_objects; self.max_bytes=max_bytes
        self.records=[]; self._unique={}; self.total_bytes=0
    def _path(self,digest: str) -> Path:
        hexv=digest.split(":",1)[1]
        return self.root/"objects/sha256"/hexv[:2]/f"{hexv[2:]}.blob"
    def put(self,*,logical_id: str,artifact_class: str,media_type: str,payload: bytes,semantic_digest: str|None,source_path: str) -> dict[str,Any]:
        blob_digest=digest_bytes(payload); path=self._path(blob_digest)
        if blob_digest not in self._unique:
            if len(self._unique)+1>self.max_objects:
                raise BudgetError("store object budget exceeded")
            if self.total_bytes+len(payload)>self.max_bytes:
                raise BudgetError("store byte budget exceeded")
            path.parent.mkdir(parents=True,exist_ok=True)
            if path.exists() or path.is_symlink():
                raise StoreError("unexpected preexisting CAS path")
            tmp=path.with_name(path.name+".tmp")
            tmp.write_bytes(payload)
            os.replace(tmp,path)
            path.chmod(0o444)
            self._unique[blob_digest]={"path":path.relative_to(self.root).as_posix(),"size_bytes":len(payload)}
            self.total_bytes+=len(payload)
        else:
            if path.read_bytes()!=payload:
                raise StoreError("digest collision or object corruption")
        body={"schema_version":"1.0.0","object_id":stable_id("OBJECT",logical_id,blob_digest),"logical_id":logical_id,"artifact_class":artifact_class,"media_type":media_type,"blob_digest":blob_digest,"semantic_digest":semantic_digest,"size_bytes":len(payload),"store_path":self._unique[blob_digest]["path"],"source_path":source_path,"immutable":True}
        rec={**body,"record_digest":digest_object(body)}
        self.records.append(rec)
        return rec
    def index(self) -> dict[str,Any]:
        ordered=sorted(self.records,key=lambda x:(x["logical_id"],x["blob_digest"]))
        body={"schema_version":"1.0.0","addressing":"SHA256_EXACT_BYTES","object_count":len(self._unique),"reference_count":len(ordered),"total_bytes":self.total_bytes,"objects":ordered,"overwrite_allowed":False,"symlinks_allowed":False}
        return {**body,"object_index_digest":digest_object(body)}
