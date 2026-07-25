from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[3]
output=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'decision-alpha-lab-saed-v4-06-treatment-dsl-v1.0.0.zip'
paths=[x.strip() for x in (ROOT/'releases/history/saed/indexes/SAED_V4_06_FILE_INDEX.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for relative in paths:
        source=ROOT/relative
        if not source.is_file(): raise SystemExit(f'indexed file missing: {relative}')
        archive.write(source,relative)
print(output)
