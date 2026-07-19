from __future__ import annotations
import re
from pathlib import Path
MQL_FUNCTION=re.compile(r'(?m)^\s*(?:static\s+)?(?:bool|void|int|long|double|string|datetime|color|ENUM_[A-Za-z0-9_]+|[A-Za-z_][A-Za-z0-9_<>]*)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*(?:const\s*)?\{')
PY_FUNCTION=re.compile(r'(?m)^\s*(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(')
MQL_INPUT=re.compile(r'(?m)^\s*input\s+(?:group\s+"[^"]*"\s*)?(?:[A-Za-z_][A-Za-z0-9_<>]*\s+)+([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|;)')
PREFIX_ASSIGN=re.compile(r'(?i)\b[A-Za-z_][A-Za-z0-9_]*(?:prefix|object_prefix|obj_prefix)[A-Za-z0-9_]*\s*=\s*"([^"]{1,96})"')
OBJECT_CALL=re.compile(r'(?s)\b(?:ObjectCreate|ObjectFind|ObjectDelete|ObjectSet\w*|ObjectGet\w*)\s*\([^,]*,\s*"([^"]{1,96})"')
EXPERIMENT=re.compile(r'\b(?:EXP\d{4}|M\d{4}|E\d{4}|A\d{4}|I\d{2}|ACL\d{2}|LCM\d{2})\b',re.I)

def extract(path: Path, rel: str) -> dict[str,list[str]]:
    if path.suffix.lower() not in {'.mq5','.mqh','.py'}: return {'functions':[],'inputs':[],'object_prefixes':[],'experiment_codes':[]}
    try: text=path.read_text(encoding='utf-8',errors='replace')
    except OSError: return {'functions':[],'inputs':[],'object_prefixes':[],'experiment_codes':[]}
    funcs=MQL_FUNCTION.findall(text) if path.suffix.lower() in {'.mq5','.mqh'} else PY_FUNCTION.findall(text)
    inputs=MQL_INPUT.findall(text) if path.suffix.lower() in {'.mq5','.mqh'} else []
    prefixes=PREFIX_ASSIGN.findall(text)+OBJECT_CALL.findall(text)
    codes=EXPERIMENT.findall(rel)
    return {k:sorted(set(v),key=lambda x:(x.casefold(),x)) for k,v in {'functions':funcs,'inputs':inputs,'object_prefixes':prefixes,'experiment_codes':codes}.items()}
