from pathlib import Path
import hashlib
def fd(p):
 h=hashlib.sha256(p.read_bytes()).hexdigest();return "sha256:"+h
def verify(root:Path,ledger:Path):
 errs=[];n=0
 for line in ledger.read_text().splitlines():
  if not line.strip():continue
  expected,rel=line.split("  ",1);p=root/rel;n+=1
  if not p.is_file():errs.append({"path":rel,"error":"MISSING"})
  elif fd(p)!=expected:errs.append({"path":rel,"error":"HASH"})
 return {"passed":not errs,"checked":n,"errors":errs}
