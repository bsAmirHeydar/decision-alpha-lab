from __future__ import annotations
import json
from pathlib import Path
from .canonical import canonical_json

def dump_json(path,document):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(document,indent=2,sort_keys=True,ensure_ascii=False)+'
',encoding='utf-8');return p

def load_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))

def dump_jsonl(path,documents):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('
'.join(canonical_json(x) for x in documents)+'
',encoding='utf-8');return p
