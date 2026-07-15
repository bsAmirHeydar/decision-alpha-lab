#!/usr/bin/env python3
from pathlib import Path
import hashlib, zipfile
ROOT=Path(__file__).resolve().parents[2]
index=ROOT/'UCEE_I18_FILE_INDEX.txt'
paths=[line.strip() for line in index.read_text().splitlines() if line.strip()]
hash_file=ROOT/'UCEE_I18_FILE_HASHES.sha256'
lines=[]
for rel in paths:
    if rel=='UCEE_I18_FILE_HASHES.sha256':
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
