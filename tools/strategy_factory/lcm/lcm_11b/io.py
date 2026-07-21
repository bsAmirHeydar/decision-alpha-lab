from __future__ import annotations
import csv,json
from pathlib import Path

def load_json(path:Path):return json.loads(path.read_text(encoding="utf-8"))
def load_jsonl(path:Path):return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
def dump_json(path:Path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
def dump_jsonl(path:Path,rows):path.parent.mkdir(parents=True,exist_ok=True);path.write_text("".join(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n" for x in rows),encoding="utf-8",newline="\n")
def dump_csv(path:Path,rows,fieldnames):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fieldnames,lineterminator="\n");w.writeheader();w.writerows(rows)
