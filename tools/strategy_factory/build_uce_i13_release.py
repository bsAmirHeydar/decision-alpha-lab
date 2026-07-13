#!/usr/bin/env python3
from pathlib import Path
import hashlib, zipfile
ROOT=Path(__file__).resolve().parents[2]
paths=[x.strip() for x in (ROOT/'UCEE_I13_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
hashes=[]
for rel in paths:
    if rel=='UCEE_I13_FILE_HASHES.sha256':
        continue
    hashes.append(f"{hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()}  {rel}")
(ROOT/'UCEE_I13_FILE_HASHES.sha256').write_text('\n'.join(hashes)+'\n')
out=ROOT.parent/'decision-alpha-lab-ucee-i13-hybrid-policy-v1.0.0.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in paths:
        z.write(ROOT/rel,rel)
print(out)
