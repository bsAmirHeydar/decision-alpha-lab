from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(Path(__file__).parent))
from _schema_validator import validate
m=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_21/CONTRACT_VALIDATION_MAP.JSON').read_text(encoding='utf-8'))
for p in m['pairs']:
 d=json.loads((ROOT/p['document']).read_text(encoding='utf-8'));s=json.loads((ROOT/p['schema']).read_text(encoding='utf-8'));validate(d,s)
print(json.dumps({'passed':True,'closed_schema_pairs':len(m['pairs'])},sort_keys=True))
