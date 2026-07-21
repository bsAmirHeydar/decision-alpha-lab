from __future__ import annotations
import ast
from pathlib import Path
from .constants import FORBIDDEN_AUTHORITY_TOKENS

def validate_python(root:Path)->dict:
    errors=[]; files=sorted(root.glob('*.py'))
    for path in files:
        text=path.read_text(encoding='utf-8')
        try: ast.parse(text,filename=path.as_posix())
        except SyntaxError as exc: errors.append({"path":path.as_posix(),"error":str(exc)})
        for token in FORBIDDEN_AUTHORITY_TOKENS:
            if token in text: errors.append({"path":path.as_posix(),"error":f'FORBIDDEN_AUTHORITY_TOKEN:{token}'})
    return {"result":"PASS" if files and not errors else "FAIL","file_count":len(files),"errors":errors}
