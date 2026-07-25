from __future__ import annotations
import hashlib,json
from pathlib import Path
def load_json(path:Path):return json.loads(path.read_text(encoding='utf-8'))
def load_jsonl(path:Path):return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
def file_digest(path:Path)->str:
 h=hashlib.sha256()
 with path.open('rb') as fh:
  for chunk in iter(lambda:fh.read(1024*1024),b''):h.update(chunk)
 return 'sha256:'+h.hexdigest()
