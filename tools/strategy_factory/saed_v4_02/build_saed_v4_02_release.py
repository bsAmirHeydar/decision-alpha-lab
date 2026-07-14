from pathlib import Path
import zipfile,sys
ROOT=Path(__file__).resolve().parents[3]
out=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'decision-alpha-lab-saed-v4-02-context-digital-twin-v1.0.0.zip'
paths=[x.strip() for x in (ROOT/'SAED_V4_02_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in paths:z.write(ROOT/p,p)
print(out)
