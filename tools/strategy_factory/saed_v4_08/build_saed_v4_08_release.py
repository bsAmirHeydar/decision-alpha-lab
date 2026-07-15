from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[3];name='decision-alpha-lab-saed-v4-08-executable-path-outcome-cube-v1.0.0.zip';index=[x.strip() for x in (ROOT/'SAED_V4_08_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
with zipfile.ZipFile(ROOT/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for rel in index:z.write(ROOT/rel,rel)
print(ROOT/name)
