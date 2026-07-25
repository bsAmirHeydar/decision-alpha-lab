from pathlib import Path
import hashlib,zipfile
root=Path(__file__).resolve().parents[2]
index=root/'releases/history/exp0019/indexes/EXP0019_FP_I12_FILE_INDEX.txt'
out=root.parent/'decision-alpha-lab-exp0019-faerie-protocol-fp-i12-operator-ux-v1.0.0.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for r in index.read_text(encoding='utf-8').splitlines():
  if r.strip(): z.write(root/r,r)
print(out,hashlib.sha256(out.read_bytes()).hexdigest())
