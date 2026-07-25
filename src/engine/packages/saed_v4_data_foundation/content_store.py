from __future__ import annotations
from pathlib import Path
import os,tempfile
from .canonical import sha256_bytes
from .errors import IntegrityViolation
class ContentAddressedStore:
    def __init__(self,root:str|Path): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def _path(self,digest:str)->Path: return self.root/digest[:2]/digest[2:4]/digest
    def put_bytes(self,data:bytes)->str:
        digest=sha256_bytes(data); target=self._path(digest); target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():
            if target.read_bytes()!=data: raise IntegrityViolation('content-address collision or corruption')
            return digest
        fd,tmp=tempfile.mkstemp(dir=target.parent,prefix='.tmp-')
        try:
            with os.fdopen(fd,'wb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
            os.replace(tmp,target)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        return digest
    def put_text(self,text:str)->str: return self.put_bytes(text.encode('utf-8'))
    def get_bytes(self,digest:str)->bytes:
        p=self._path(digest)
        if not p.is_file(): raise FileNotFoundError(digest)
        data=p.read_bytes()
        if sha256_bytes(data)!=digest: raise IntegrityViolation('stored content hash mismatch')
        return data
    def verify(self,digest:str)->bool:
        try: return sha256_bytes(self.get_bytes(digest))==digest
        except (FileNotFoundError,IntegrityViolation): return False
    def has(self,digest:str)->bool: return self._path(digest).is_file()
