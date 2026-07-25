from __future__ import annotations
import re
from pathlib import Path
from .canonical import with_digest,digest_file
SECRET_PATTERNS=[('PEM_PRIVATE_KEY',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),('AWS_ACCESS_KEY',re.compile(r'AKIA[0-9A-Z]{16}')),('GITHUB_TOKEN',re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}')),('GENERIC_PASSWORD_ASSIGNMENT',re.compile(r'(?i)(?:password|passwd|secret)\s*[:=]\s*["\'][^"\']{8,}["\']'))]
FORBIDDEN_MQL5=['OrderSend(','CTrade','PositionOpen(','WebRequest(','Buy(','Sell(']
def scan_secrets(root:Path)->dict:
    findings=[]; scanned=0
    for p in sorted(x for x in root.rglob('*') if x.is_file() and not x.is_symlink()):
        if p.stat().st_size>2_000_000: continue
        try: text=p.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        scanned+=1
        for pid,pat in SECRET_PATTERNS:
            if pat.search(text): findings.append({'path':p.relative_to(root).as_posix(),'pattern_id':pid})
    return with_digest({'schema_version':'1.0.0','scan_type':'SECRET_SCAN','files_scanned':scanned,'finding_count':len(findings),'findings':findings,'passed':not findings},'scan_digest')
def scan_paths(root:Path)->dict:
    symlinks=[]; escapes=[]; files=0
    for p in root.rglob('*'):
        if p.is_symlink(): symlinks.append(p.relative_to(root).as_posix())
        elif p.is_file(): files+=1
    return with_digest({'schema_version':'1.0.0','scan_type':'PATH_AND_SYMLINK_SCAN','files_scanned':files,'symlink_count':len(symlinks),'symlinks':symlinks,'path_escape_count':len(escapes),'path_escapes':escapes,'passed':not symlinks and not escapes},'scan_digest')
def scan_mql5(root:Path)->dict:
    findings=[]; scanned=0
    for p in sorted(x for x in root.rglob('*') if x.is_file() and x.suffix.lower() in {'.mq5','.mqh'}):
        text=p.read_text(encoding='utf-8',errors='ignore'); scanned+=1
        for token in FORBIDDEN_MQL5:
            if token in text: findings.append({'path':p.relative_to(root).as_posix(),'token':token})
    return with_digest({'schema_version':'1.0.0','scan_type':'MQL5_FORBIDDEN_API_SCAN','files_scanned':scanned,'finding_count':len(findings),'findings':findings,'passed':not findings},'scan_digest')
def scan_static(root:Path)->dict:
    findings=[]; scanned=0
    patterns=[('DYNAMIC_EVAL',re.compile(r'\beval\s*\(')),('DYNAMIC_EXEC',re.compile(r'\bexec\s*\(')),('SHELL_TRUE',re.compile(r'shell\s*=\s*True')),('UNSAFE_PICKLE',re.compile(r'pickle\.loads?\s*\('))]
    for p in sorted(x for x in root.rglob('*.py') if x.is_file() and not x.is_symlink()):
        text=p.read_text(encoding='utf-8',errors='ignore'); scanned+=1
        for pid,pat in patterns:
            if pat.search(text): findings.append({'path':p.relative_to(root).as_posix(),'pattern_id':pid})
    return with_digest({'schema_version':'1.0.0','scan_type':'REFERENCE_STATIC_SCAN','files_scanned':scanned,'finding_count':len(findings),'findings':findings,'passed':not findings,'claim':'PATTERN_SCAN_NOT_FULL_SAST'},'scan_digest')
