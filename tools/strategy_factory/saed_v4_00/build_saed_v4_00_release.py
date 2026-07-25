#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
INDEX=ROOT/'releases/history/saed/indexes/SAED_V4_00_FILE_INDEX.txt'; LEDGER=ROOT/'releases/history/saed/hashes/SAED_V4_00_FILE_HASHES.sha256'
files=[x.strip() for x in INDEX.read_text(encoding='utf-8').splitlines() if x.strip()]
lines=[]
for rel in files:
 if rel=='releases/history/saed/hashes/SAED_V4_00_FILE_HASHES.sha256': continue
 lines.append(f"{hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()}  {rel}")
LEDGER.write_text('\n'.join(lines)+'\n',encoding='utf-8')
out=Path('/mnt/data/decision-alpha-lab-saed-v4-00-program-constitution-v1.0.0.zip')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in files: z.write(ROOT/rel,rel)
print(json.dumps({'output':str(out),'files':len(files),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))
