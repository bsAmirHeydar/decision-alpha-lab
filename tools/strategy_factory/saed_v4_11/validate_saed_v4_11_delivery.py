from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'releases/history/saed/indexes/SAED_V4_11_FILE_INDEX.txt';ledger=ROOT/'releases/history/saed/hashes/SAED_V4_11_FILE_HASHES.sha256';manifest_path=ROOT/'releases/history/saed/manifests/SAED_V4_11_PATCH_MANIFEST.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file()
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths))
missing=[x for x in paths if not (ROOT/x).is_file()]
assert not missing,missing
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
 if not line.strip():continue
 digest,path=line.split('  ',1);expected[path]=digest
for path,digest in expected.items():
 actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest();assert actual==digest,(path,digest,actual)
assert set(expected)==set(paths)-{'releases/history/saed/hashes/SAED_V4_11_FILE_HASHES.sha256'}
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
assert manifest['phase']=='SAED_V4_11' and manifest['version']=='1.0.0'
assert manifest['file_count']==len(paths) and manifest['hash_count']==len(expected)
assert manifest['qa_passed'] is True and manifest['implementation_status']=='implemented_reference_synthetic'
status=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_11.json').read_text())
assert status['claims']['learned_reference_representation'] is True
assert status['claims']['real_corpus_training'] is False and status['claims']['production_authorization'] is False
print(f"V4-11 delivery validated: {len(paths)} files, {len(expected)} hashes")
