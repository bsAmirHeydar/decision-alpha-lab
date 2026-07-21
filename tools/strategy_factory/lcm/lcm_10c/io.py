from __future__ import annotations
import json
from pathlib import Path
from typing import Any,Iterable

def load_json(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def load_jsonl(path:Path)->list[dict]:return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
def dump_json(path:Path,value:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
def dump_jsonl(path:Path,rows:Iterable[dict])->None:
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text("".join(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n" for x in rows),encoding="utf-8",newline="\n")
def lines(path:Path)->list[str]:return [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
