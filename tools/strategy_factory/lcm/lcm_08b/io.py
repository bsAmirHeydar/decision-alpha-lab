from __future__ import annotations
import csv,json,os,shutil,tempfile
from pathlib import Path

def write_json(path:Path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
def write_jsonl(path:Path,rows):path.parent.mkdir(parents=True,exist_ok=True);path.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in rows),encoding="utf-8")
def write_text(path:Path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding="utf-8",newline="\n")
def write_csv(path:Path,rows,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
