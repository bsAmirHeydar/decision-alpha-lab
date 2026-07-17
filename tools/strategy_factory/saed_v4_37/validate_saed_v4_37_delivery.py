from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; idx=ROOT/'SAED_V4_37_FILE_INDEX.txt'; hashes=ROOT/'SAED_V4_37_FILE_HASHES.sha256'; manifest=ROOT/'SAED_V4_37_PATCH_MANIFEST.json'
for p in [idx,hashes,manifest,ROOT/'SAED_V4_37_QA_REPORT.json',ROOT/'SAED_V4_37_ARTIFACT_INVENTORY.csv']:
 if not p.exists():raise SystemExit(f'missing {p.name}')
paths=[x for x in idx.read_text().splitlines() if x]
missing=[x for x in paths if not (ROOT/x).exists()]
if missing:raise SystemExit(f'missing indexed files: {missing[:5]}')
for line in hashes.read_text().splitlines():
 if not line:continue
 expected,rel=line.split('  ',1); actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
 if expected!=actual:raise SystemExit(f'hash mismatch {rel}')
m=json.loads(manifest.read_text())
if m['phase']!='SAED_V4_37' or m['next_phase']!='SAED_V4_38' or m['production_authorization'] is not False:raise SystemExit('manifest boundary invalid')
print(json.dumps({'phase':'SAED_V4_37','indexed_files':len(paths),'hash_entries':len(hashes.read_text().splitlines()),'passed':True}))
