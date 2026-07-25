#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import hashlib, zipfile
ROOT=find_repository_root(__file__)
paths=[x.strip() for x in (ROOT/'releases/history/ucee/indexes/UCEE_I13_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
hashes=[]
for rel in paths:
    if rel=='releases/history/ucee/hashes/UCEE_I13_FILE_HASHES.sha256':
        continue
    hashes.append(f"{hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()}  {rel}")
(ROOT/'releases/history/ucee/hashes/UCEE_I13_FILE_HASHES.sha256').write_text('\n'.join(hashes)+'\n')
out=ROOT.parent/'decision-alpha-lab-ucee-i13-hybrid-policy-v1.0.0.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in paths:
        z.write(ROOT/rel,rel)
print(out)
