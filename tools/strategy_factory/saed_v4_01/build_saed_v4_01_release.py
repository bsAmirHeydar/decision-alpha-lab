#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT.parent/'decision-alpha-lab-saed-v4-01-sovereign-data-foundation-v1.0.0.zip';idx=ROOT/'SAED_V4_01_FILE_INDEX.txt';files=[x.strip() for x in idx.read_text().splitlines() if x.strip()]
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for rel in files:z.write(ROOT/rel,rel)
print(json.dumps({'zip':str(OUT),'files':len(files),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2))
