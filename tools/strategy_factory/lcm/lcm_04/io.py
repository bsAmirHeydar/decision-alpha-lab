from __future__ import annotations
import csv,json,os,shutil,tempfile
from pathlib import Path
from typing import Iterable,Mapping,Any

def read_json(path: Path): return json.loads(path.read_text(encoding='utf-8'))
def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip(): yield json.loads(line)
def read_csv(path: Path):
    with path.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def write_json(path: Path,obj: Any):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def write_jsonl(path: Path,rows: Iterable[Mapping[str,Any]]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='\n') as f:
        for row in rows: f.write(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
def write_csv(path: Path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def write_text(path: Path,text: str):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
def private_staging(parent: Path,prefix: str):
    parent.mkdir(parents=True,exist_ok=True);return Path(tempfile.mkdtemp(prefix=prefix,dir=parent))
def atomic_publish(staging: Path,final: Path):
    if final.exists(): raise FileExistsError(f'destination exists: {final}')
    os.replace(staging,final)
