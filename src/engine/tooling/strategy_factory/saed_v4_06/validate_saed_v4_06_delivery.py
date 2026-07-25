from tools.repository_paths import find_repository_root
from pathlib import Path
import hashlib
import json

ROOT=find_repository_root(__file__)
index=[x.strip() for x in (ROOT/'releases/history/saed/indexes/SAED_V4_06_FILE_INDEX.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
if index!=sorted(set(index)): raise SystemExit('file index must be sorted and unique')
missing=[p for p in index if not (ROOT/p).is_file()]
if missing: raise SystemExit('missing indexed files: '+','.join(missing))
expected={}
for line in (ROOT/'releases/history/saed/hashes/SAED_V4_06_FILE_HASHES.sha256').read_text(encoding='utf-8').splitlines():
    if line.strip():
        digest,relative=line.split('  ',1);expected[relative]=digest
errors=[]
for relative,digest in expected.items():
    path=ROOT/relative
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest: errors.append(relative)
if errors: raise SystemExit('hash mismatch: '+','.join(errors))
manifest=json.loads((ROOT/'releases/history/saed/manifests/SAED_V4_06_PATCH_MANIFEST.json').read_text(encoding='utf-8'))
if manifest['file_count']!=len(index): raise SystemExit('manifest count mismatch')
if manifest['hash_count']!=len(expected): raise SystemExit('manifest hash count mismatch')
if set(expected)!=set(index)-{'releases/history/saed/hashes/SAED_V4_06_FILE_HASHES.sha256'}: raise SystemExit('hash ledger coverage mismatch')
print(f'delivery validation passed for {len(index)} indexed files and {len(expected)} hashes')
