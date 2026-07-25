#!/usr/bin/env python3
from pathlib import Path
import hashlib,zipfile
ROOT=Path(__file__).resolve().parents[2];paths=[x.strip() for x in (ROOT/'releases/history/ucee/indexes/UCEE_I14_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
h=[]
for rel in paths:
 if rel=='releases/history/ucee/hashes/UCEE_I14_FILE_HASHES.sha256':continue
 h.append(f"{hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()}  {rel}")
(ROOT/'releases/history/ucee/hashes/UCEE_I14_FILE_HASHES.sha256').write_text('\n'.join(h)+'\n')
out=ROOT.parent/'decision-alpha-lab-ucee-i14-immutable-runtime-v1.0.0.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in paths:z.write(ROOT/rel,rel)
print(out)
