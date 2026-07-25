from pathlib import Path
import sys,zipfile
ROOT=Path(__file__).resolve().parents[3];output=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'decision-alpha-lab-saed-v4-07-constraint-solver-action-lattice-v1.0.0.zip';paths=[x.strip() for x in (ROOT/'releases/history/saed/indexes/SAED_V4_07_FILE_INDEX.txt').read_text().splitlines() if x.strip()]
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for rel in paths:
  p=ROOT/rel
  if not p.is_file():raise SystemExit(f'indexed file missing: {rel}')
  z.write(p,rel)
print(output)
