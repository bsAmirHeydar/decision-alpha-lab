from __future__ import annotations
from pathlib import Path
from .canonical import sha256_file

def verify_mt5_run(root: str|Path):
    root=Path(root).resolve(); ledger=root/'MT5_RUN_FILE_HASHES.sha256'; marker=root/'MT5_RUN_COMPLETE'; manifest=root/'mt5_run_manifest.json'
    if not all(x.is_file() for x in (ledger,marker,manifest)): return {'status':'FAIL','errors':['run_incomplete']}
    errors=[]; count=0
    for line in ledger.read_text(encoding='utf-8').splitlines():
        if not line: continue
        prefix,rel=line.split('  ',1); path=root/rel
        if not path.is_file(): errors.append('missing:'+rel); continue
        if sha256_file(path)!=prefix.removeprefix('sha256:'): errors.append('hash_mismatch:'+rel)
        else: count+=1
    return {'status':'PASS' if not errors else 'FAIL','errors':errors,'verified_file_count':count,'run_root':root.as_posix()}
