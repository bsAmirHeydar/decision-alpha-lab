from __future__ import annotations
import ast
from pathlib import Path
FORBIDDEN_IMPORTS={"subprocess","socket","requests","urllib","http.client","MetaTrader5"}
def scan_module(root:Path)->dict:
    errors=[]
    for p in sorted(root.rglob("*.py")):
        try:tree=ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError as e:errors.append({"path":p.as_posix(),"code":"SYNTAX_ERROR","detail":str(e)});continue
        for n in ast.walk(tree):
            if isinstance(n,(ast.Import,ast.ImportFrom)):
                names=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module or ""]
                for name in names:
                    if any(name==x or name.startswith(x+".") for x in FORBIDDEN_IMPORTS):errors.append({"path":p.as_posix(),"code":"FORBIDDEN_IMPORT","detail":name})
    return {"passed":not errors,"error_count":len(errors),"errors":errors}
