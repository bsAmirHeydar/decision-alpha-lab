from __future__ import annotations
from pathlib import Path
from .canonical import file_digest

def verify_hash_ledger(repo_root:Path,ledger:Path)->dict:
    errors=[];count=0
    for line in ledger.read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        expected,rel=line.split('  ',1);p=repo_root/rel
        if not p.is_file():errors.append({'path':rel,'error':'MISSING'})
        elif file_digest(p)!=expected:errors.append({'path':rel,'error':'DIGEST_MISMATCH'})
        count+=1
    return {'checked':count,'errors':errors,'result':'PASS' if not errors else 'FAIL'}
