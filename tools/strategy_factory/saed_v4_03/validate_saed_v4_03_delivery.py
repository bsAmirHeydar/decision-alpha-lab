from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
idx=[x.strip() for x in (ROOT/'SAED_V4_03_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
missing=[p for p in idx if not (ROOT/p).is_file()]
if missing:raise SystemExit('missing indexed files: '+','.join(missing))
expected={}
for line in (ROOT/'SAED_V4_03_FILE_HASHES.sha256').read_text().splitlines():
 if not line.strip():continue
 h,p=line.split('  ',1);expected[p]=h
errors=[]
for p,h in expected.items():
 q=ROOT/p
 if not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest()!=h:errors.append(p)
if errors:raise SystemExit('hash mismatch: '+','.join(errors))
manifest=json.loads((ROOT/'SAED_V4_03_PATCH_MANIFEST.json').read_text())
if manifest['file_count']!=len(idx):raise SystemExit('manifest count mismatch')
print(f'delivery validation passed for {len(idx)} indexed files and {len(expected)} hashes')
