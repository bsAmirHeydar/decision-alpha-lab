from __future__ import annotations
import json,os,tempfile
from pathlib import Path
from typing import Any
from .errors import IntegrityError

def load_json(path:Path)->dict[str,Any]:
    if not path.is_file() or path.is_symlink():
        raise IntegrityError(f'ACL15_JSON_NOT_REGULAR:{path}')
    value=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value,dict):
        raise IntegrityError(f'ACL15_JSON_OBJECT_REQUIRED:{path}')
    return value

def dump_json(path:Path,obj:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

def safe_rel(path:str)->str:
    p=Path(path)
    if not path or p.is_absolute() or '..' in p.parts:
        raise IntegrityError('ACL15_UNSAFE_PATH')
    return p.as_posix()

def new_staging(destination:Path)->Path:
    if destination.exists():
        raise IntegrityError('ACL15_DESTINATION_EXISTS')
    destination.parent.mkdir(parents=True,exist_ok=True)
    return Path(tempfile.mkdtemp(prefix='.acl15-staging-',dir=destination.parent))

def atomic_publish(staging:Path,destination:Path)->None:
    os.replace(staging,destination)
