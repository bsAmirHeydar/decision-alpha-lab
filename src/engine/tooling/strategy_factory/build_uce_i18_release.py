#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import hashlib, zipfile
ROOT=find_repository_root(__file__)
index=ROOT/'releases/history/ucee/indexes/UCEE_I18_FILE_INDEX.txt'
paths=[line.strip() for line in index.read_text().splitlines() if line.strip()]
hash_file=ROOT/'releases/history/ucee/hashes/UCEE_I18_FILE_HASHES.sha256'
lines=[]
for rel in paths:
    if rel=='releases/history/ucee/hashes/UCEE_I18_FILE_HASHES.sha256':
        continue
    path=ROOT/rel
    if not path.is_file():
        raise FileNotFoundError(rel)
    lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}")
hash_file.write_text("\n".join(lines)+"\n",encoding='utf-8')
out=ROOT.parent/'decision-alpha-lab-ucee-i18-production-qualification-v1.0.0.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as archive:
    for rel in paths:
        archive.write(ROOT/rel,rel)
print(out)
