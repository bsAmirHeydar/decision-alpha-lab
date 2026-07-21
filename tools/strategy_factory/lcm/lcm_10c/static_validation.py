from __future__ import annotations
import ast
from pathlib import Path

def validate_python(root:Path)->dict:
    errors=[];count=0
    for p in sorted(root.glob('*.py')):
        try:ast.parse(p.read_text(encoding='utf-8'),filename=p.as_posix());count+=1
        except SyntaxError as e:errors.append({'path':p.as_posix(),'error':str(e)})
    return {'file_count':count,'errors':errors,'result':'PASS' if not errors else 'FAIL'}
