from tools.repository_paths import find_repository_root
from pathlib import Path
import hashlib,json
ROOT=find_repository_root(__file__);index=ROOT/'releases/history/saed/indexes/SAED_V4_14_FILE_INDEX.txt';ledger=ROOT/'releases/history/saed/hashes/SAED_V4_14_FILE_HASHES.sha256';manifest_path=ROOT/'releases/history/saed/manifests/SAED_V4_14_PATCH_MANIFEST.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file();paths=[x.strip() for x in index.read_text().splitlines() if x.strip()];assert len(paths)==len(set(paths));assert not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text().splitlines():
 if line.strip():d,p=line.split('  ',1);expected[p]=d
for p,d in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,p
assert set(expected)==set(paths)-{'releases/history/saed/hashes/SAED_V4_14_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text());assert m['phase']=='SAED_V4_14' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed']
s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_14.json').read_text());assert s['claims']['foundation_model_adapter_boundary_implemented'] and not s['claims']['production_authorization']
print(f'V4-14 delivery validated: {len(paths)} files, {len(expected)} hashes')
