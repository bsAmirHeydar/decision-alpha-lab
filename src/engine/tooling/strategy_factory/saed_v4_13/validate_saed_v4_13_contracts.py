from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(Path(__file__).parent));from _schema_validator import validate
m=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_13/CONTRACT_VALIDATION_MAP.JSON').read_text());count=0
for pair in m['pairs']:
 s=json.loads((ROOT/pair['schema']).read_text());d=json.loads((ROOT/pair['document']).read_text());validate(d,s);assert s.get('$schema');assert s.get('type')!='object' or s.get('additionalProperties') is False;count+=1
print(f'validated {count} closed SAED V4-13 schema/document pairs')
