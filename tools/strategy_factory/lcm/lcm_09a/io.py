from __future__ import annotations
import json
from pathlib import Path
def load_json(p:Path): return json.loads(p.read_text(encoding="utf-8"))
def load_jsonl(p:Path): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def nonempty_lines(p:Path): return [x.strip() for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
