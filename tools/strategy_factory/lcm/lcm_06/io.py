from __future__ import annotations
import csv,json,os,shutil,tempfile
from pathlib import Path

def write_json(path:Path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
def write_jsonl(path:Path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="\n") as f:
        for row in rows:f.write(json.dumps(row,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n")
def write_csv(path:Path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");wr.writeheader();wr.writerows(rows)
def write_text(path:Path,text): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding="utf-8")
def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8-sig"))
def read_jsonl(path):
    with Path(path).open(encoding="utf-8-sig") as f:return [json.loads(x) for x in f if x.strip()]
def read_csv(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def private_staging(parent:Path,prefix):parent.mkdir(parents=True,exist_ok=True);return Path(tempfile.mkdtemp(prefix=prefix,dir=parent))
def atomic_publish(staging:Path,final:Path):
    if final.exists():raise FileExistsError(f"destination exists: {final}")
    os.replace(staging,final);return final
def cleanup(path):
    if Path(path).exists():shutil.rmtree(path)
