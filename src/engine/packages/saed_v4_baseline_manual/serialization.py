import json
from pathlib import Path

def load_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write_json(path,value):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
