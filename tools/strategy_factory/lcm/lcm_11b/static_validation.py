from __future__ import annotations
import ast
from pathlib import Path
from .constants import FORBIDDEN_AUTHORITY_TOKENS
def validate_python(root:Path)->dict:
    errors=[];files=sorted(root.glob("*.py"))
    for p in files:
        text=p.read_text(encoding="utf-8")
        try:ast.parse(text,filename=p.as_posix())
        except SyntaxError as exc:errors.append({"path":p.as_posix(),"error":str(exc)})
        for token in FORBIDDEN_AUTHORITY_TOKENS:
            if token in text:errors.append({"path":p.as_posix(),"error":"FORBIDDEN_AUTHORITY_TOKEN:"+token})
    return {"result":"PASS" if files and not errors else "FAIL","file_count":len(files),"errors":errors}
