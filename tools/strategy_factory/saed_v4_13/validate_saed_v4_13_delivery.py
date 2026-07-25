from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3];index=ROOT/'releases/history/saed/indexes/SAED_V4_13_FILE_INDEX.txt';ledger=ROOT/'releases/history/saed/hashes/SAED_V4_13_FILE_HASHES.sha256';manifest_path=ROOT/'releases/history/saed/manifests/SAED_V4_13_PATCH_MANIFEST.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file();paths=[x.strip() for x in index.read_text().splitlines() if x.strip()];assert len(paths)==len(set(paths));assert not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text().splitlines():
 if line.strip():d,p=line.split('  ',1);expected[p]=d
for p,d in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,p
assert set(expected)==set(paths)-{'releases/history/saed/hashes/SAED_V4_13_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text());assert m['phase']=='SAED_V4_13' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed']
s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_13.json').read_text());assert s['claims']['graph_hypergraph_reference_implemented'] and not s['claims']['production_authorization']
print(f'V4-13 delivery validated: {len(paths)} files, {len(expected)} hashes')
