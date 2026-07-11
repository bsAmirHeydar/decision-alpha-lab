from __future__ import annotations
from pathlib import Path
import json

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write_json(path,value):
    Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+"\n",encoding="utf-8")
