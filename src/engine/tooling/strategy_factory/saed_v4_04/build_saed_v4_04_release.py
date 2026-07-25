from tools.repository_paths import find_repository_root
from pathlib import Path
import zipfile,sys
ROOT=find_repository_root(__file__)
out=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'decision-alpha-lab-saed-v4-04-multimodal-view-platform-v1.0.0.zip'
paths=[x.strip() for x in (ROOT/'releases/history/saed/indexes/SAED_V4_04_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in paths:z.write(ROOT/p,p)
print(out)
