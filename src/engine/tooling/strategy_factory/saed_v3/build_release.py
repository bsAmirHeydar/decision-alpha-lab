from pathlib import Path
import hashlib,zipfile,sys
root=Path(sys.argv[1]); out=Path(sys.argv[2])
files=sorted(p for p in root.rglob("*") if p.is_file())
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
    for p in files: z.write(p,p.relative_to(root).as_posix())
print(hashlib.sha256(out.read_bytes()).hexdigest(),len(files))
