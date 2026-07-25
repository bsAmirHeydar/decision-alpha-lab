from __future__ import annotations
import ast, io, re, tokenize
from pathlib import Path
from .canonical import stable_id, text_digest
from .models import FunctionRecord

MQL_FUNCTION_RE = re.compile(
    r"^\s*(?:(?:static|virtual|const|inline|template\s*<[^>]+>)\s+)*"
    r"(?:void|bool|int|uint|long|ulong|double|float|string|datetime|color|char|uchar|short|ushort|"
    r"[A-Za-z_]\w*(?:::\w+)?(?:\s*[&*])?)\s+([A-Za-z_]\w*(?:::\w+)?)\s*\([^;]*\)\s*(?:const\s*)?\{"
)
MQL_ENTRY_POINTS = {"OnInit":"MQL5_ON_INIT", "OnDeinit":"MQL5_ON_DEINIT", "OnTick":"MQL5_ON_TICK", "OnTimer":"MQL5_ON_TIMER", "OnTrade":"MQL5_ON_TRADE", "OnTradeTransaction":"MQL5_ON_TRADE_TRANSACTION", "OnBookEvent":"MQL5_ON_BOOK_EVENT", "OnChartEvent":"MQL5_ON_CHART_EVENT", "OnStart":"MQL5_ON_START", "OnCalculate":"MQL5_ON_CALCULATE"}
CALL_RE = re.compile(r"\b([A-Za-z_]\w*(?:::\w+)?)\s*\(")
CONTROL_WORDS = {"if","for","while","switch","return","sizeof","Print","PrintFormat","ArraySize","MathMax","MathMin"}

def strip_mql_comments(text: str) -> str:
    out=[]; i=0; in_block=False; in_string=False; quote=''
    while i < len(text):
        c=text[i]; n=text[i+1] if i+1<len(text) else ''
        if in_block:
            if c=='*' and n=='/': in_block=False; out.extend('  '); i+=2
            else: out.append('\n' if c=='\n' else ' '); i+=1
            continue
        if in_string:
            out.append(c)
            if c==quote and (i==0 or text[i-1] != '\\'): in_string=False
            i+=1; continue
        if c in {'"', "'"}: in_string=True; quote=c; out.append(c); i+=1; continue
        if c=='/' and n=='*': in_block=True; out.extend('  '); i+=2; continue
        if c=='/' and n=='/':
            while i<len(text) and text[i]!='\n': out.append(' '); i+=1
            continue
        out.append(c); i+=1
    return ''.join(out)

def mql_functions(path: str, text: str) -> list[FunctionRecord]:
    clean=strip_mql_comments(text); lines=clean.splitlines(); starts=[]
    for idx,line in enumerate(lines,1):
        m=MQL_FUNCTION_RE.match(line)
        if m: starts.append((idx,m.group(1)))
    records=[]
    for pos,(start,name) in enumerate(starts):
        end=(starts[pos+1][0]-1) if pos+1<len(starts) else len(lines)
        body='\n'.join(lines[start-1:end]); calls=sorted({m.group(1).split('::')[-1] for m in CALL_RE.finditer(body) if m.group(1) not in CONTROL_WORDS and m.group(1).split('::')[-1] != name.split('::')[-1]})
        entry=tuple([MQL_ENTRY_POINTS[name]]) if name in MQL_ENTRY_POINTS else ()
        records.append(FunctionRecord(stable_id('SYMBOL',path,name,start),path,'MQL5',name,name,start,end,tuple(calls),entry))
    return records

def python_functions(path: str, text: str) -> tuple[list[FunctionRecord], str | None]:
    try: tree=ast.parse(text, filename=path)
    except SyntaxError as exc: return [], f"{exc.msg}@{exc.lineno}:{exc.offset}"
    records=[]
    class Visitor(ast.NodeVisitor):
        def __init__(self): self.stack=[]
        def _add(self,node,name):
            q='.'.join(self.stack+[name]); calls=[]
            for child in ast.walk(node):
                if isinstance(child,ast.Call):
                    fn=child.func
                    if isinstance(fn,ast.Name): calls.append(fn.id)
                    elif isinstance(fn,ast.Attribute): calls.append(fn.attr)
            entries=[]
            if name in {'main','cli','run_cli'}: entries.append('PYTHON_COMMAND_ENTRY')
            records.append(FunctionRecord(stable_id('SYMBOL',path,q,node.lineno),path,'PYTHON',name,q,node.lineno,getattr(node,'end_lineno',node.lineno),tuple(sorted(set(calls))),tuple(entries)))
            self.stack.append(name); self.generic_visit(node); self.stack.pop()
        def visit_FunctionDef(self,node): self._add(node,node.name)
        def visit_AsyncFunctionDef(self,node): self._add(node,node.name)
        def visit_ClassDef(self,node): self.stack.append(node.name); self.generic_visit(node); self.stack.pop()
    Visitor().visit(tree)
    # main guard is represented as a synthetic entry symbol so file-level calls are not lost.
    for node in tree.body:
        if isinstance(node,ast.If) and isinstance(node.test,ast.Compare):
            source=ast.get_source_segment(text,node.test) or ''
            if '__name__' in source and '__main__' in source:
                calls=[]
                for child in ast.walk(node):
                    if isinstance(child,ast.Call):
                        if isinstance(child.func,ast.Name): calls.append(child.func.id)
                        elif isinstance(child.func,ast.Attribute): calls.append(child.func.attr)
                records.append(FunctionRecord(stable_id('SYMBOL',path,'__main__',node.lineno),path,'PYTHON','__main__','__main__',node.lineno,getattr(node,'end_lineno',node.lineno),tuple(sorted(set(calls))),('PYTHON_MAIN_GUARD',)))
    return records,None

def containing_symbol(functions: list[FunctionRecord], line_number: int) -> FunctionRecord | None:
    matches=[f for f in functions if f.start_line <= line_number <= f.end_line]
    return min(matches,key=lambda f:(f.end_line-f.start_line,f.start_line)) if matches else None

def line_evidence(path: str, line_number: int, line: str, symbol: FunctionRecord | None) -> dict:
    excerpt=' '.join(line.strip().split())[:320]
    return {"path":path,"line_number":line_number,"line_digest":text_digest(line.rstrip('\r\n')),"excerpt":excerpt,"symbol_id":symbol.symbol_id if symbol else None,"symbol_name":symbol.qualified_name if symbol else None}
