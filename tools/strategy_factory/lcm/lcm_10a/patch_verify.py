from __future__ import annotations
import re
from pathlib import Path, PurePosixPath
from .canonical import file_digest
from .errors import IntegrityError
LINE=re.compile(r"^(sha256:[0-9a-f]{64})  ([^\r\n]+)$")
def _safe(raw:str)->str:
    p=PurePosixPath(raw.replace('\\','/'))
    if p.is_absolute() or not p.parts or any(x in {'','.','..'} for x in p.parts): raise IntegrityError('LCM10A_LEDGER_PATH_INVALID:'+raw)
    return p.as_posix()
def verify_hash_ledger(repo_root:Path,ledger_path:Path)->dict:
    rows=[]
    for no,line in enumerate(ledger_path.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        m=LINE.fullmatch(line)
        if not m: raise IntegrityError(f'LCM10A_LEDGER_LINE_INVALID:{no}')
        rows.append((m.group(1),_safe(m.group(2))))
    paths=[x[1] for x in rows]
    if paths!=sorted(paths) or len(paths)!=len(set(paths)): raise IntegrityError('LCM10A_LEDGER_ORDER_OR_DUPLICATE')
    bad=[]; total=0
    for expected,rel in rows:
        p=repo_root/rel
        if not p.is_file(): bad.append((rel,'MISSING')); continue
        total+=p.stat().st_size; actual=file_digest(p)
        if actual!=expected: bad.append((rel,actual))
    if bad: raise IntegrityError('LCM10A_LEDGER_MISMATCH:'+str(bad[:10]))
    return {"passed":True,"verified_file_count":len(rows),"verified_byte_count":total}
