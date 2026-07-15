from __future__ import annotations
import json
from pathlib import Path
from typing import Any
def load_json(path:str|Path)->Any:return json.loads(Path(path).read_text(encoding='utf-8'))
def dump_json(path:str|Path,value:Any)->None:Path(path).write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
