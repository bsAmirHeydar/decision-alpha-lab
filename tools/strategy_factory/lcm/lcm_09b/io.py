from __future__ import annotations
import json,os,tempfile
from pathlib import Path
from typing import Any,Iterable

def load_json(path:Path)->dict[str,Any]:return json.loads(path.read_text(encoding="utf-8"))
def load_jsonl(path:Path)->list[dict[str,Any]]:return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
def dump_json(path:Path,value:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    payload=json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as f:f.write(payload);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
def dump_jsonl(path:Path,rows:Iterable[dict[str,Any]])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    payload="".join(json.dumps(r,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n" for r in rows)
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as f:f.write(payload);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
