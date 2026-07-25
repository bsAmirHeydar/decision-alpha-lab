from tools.repository_paths import find_repository_root
from pathlib import Path
import hashlib,json
ROOT=find_repository_root(__file__);index=[x.strip() for x in (ROOT/'releases/history/saed/indexes/SAED_V4_09_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
if index!=sorted(set(index)):raise SystemExit('file index must be sorted and unique')
missing=[x for x in index if not (ROOT/x).is_file()]
if missing:raise SystemExit('missing indexed files: '+','.join(missing))
expected={}
for line in (ROOT/'releases/history/saed/hashes/SAED_V4_09_FILE_HASHES.sha256').read_text().splitlines():
 if line.strip():digest,rel=line.split('  ',1);expected[rel]=digest
errors=[rel for rel,d in expected.items() if not (ROOT/rel).is_file() or hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=d]
if errors:raise SystemExit('hash mismatch: '+','.join(errors))
m=json.loads((ROOT/'releases/history/saed/manifests/SAED_V4_09_PATCH_MANIFEST.json').read_text())
if m['file_count']!=len(index) or m['hash_count']!=len(expected):raise SystemExit('manifest count mismatch')
if set(expected)!=set(index)-{'releases/history/saed/hashes/SAED_V4_09_FILE_HASHES.sha256'}:raise SystemExit('hash ledger coverage mismatch')
print(f'delivery validation passed for {len(index)} indexed files and {len(expected)} hashes')
