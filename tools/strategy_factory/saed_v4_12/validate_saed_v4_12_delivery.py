from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'SAED_V4_12_FILE_INDEX.txt';ledger=ROOT/'SAED_V4_12_FILE_HASHES.sha256';manifest_path=ROOT/'SAED_V4_12_PATCH_MANIFEST.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file()
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()];assert len(paths)==len(set(paths));assert not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
 if line.strip():digest,path=line.split('  ',1);expected[path]=digest
for path,digest in expected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
assert set(expected)==set(paths)-{'SAED_V4_12_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text());assert m['phase']=='SAED_V4_12' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed']
s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_12.json').read_text());assert s['claims']['deep_sequence_reference_implemented'] and not s['claims']['production_authorization']
print(f"V4-12 delivery validated: {len(paths)} files, {len(expected)} hashes")
