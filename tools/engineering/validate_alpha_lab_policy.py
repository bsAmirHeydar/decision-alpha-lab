#!/usr/bin/env python3
"""Validate Decision Alpha Lab engineering-policy integration using stdlib only."""
from __future__ import annotations
import re, sys
from pathlib import Path

REQUIRED = [
    'AGENTS.md',
    'docs/engineering/ALPHA_LAB_ENGINEERING_HANDBOOK.md',
    'docs/engineering/ALPHA_LAB_POLICY_HIERARCHY.md',
    'docs/engineering/ALPHA_LAB_CODE_STYLE_STANDARD.md',
    'docs/engineering/ALPHA_LAB_QUALITY_GATE_MATRIX.md',
    'docs/engineering/ALPHA_LAB_MQL5_COMPATIBILITY_STANDARD.md',
    'docs/alpha_lab_master_architecture/ai_algorithm_engineering_os/00_START_HERE/00_Home.md',
    'docs/alpha_lab_master_architecture/ai_algorithm_engineering_os/18_ALPHA_LAB_ENGINEERING_STANDARD/_MOC.md',
    'docs/alpha_lab_master_architecture/ai_algorithm_engineering_os/19_LANGUAGE_STANDARDS/_MOC.md',
    'docs/alpha_lab_master_architecture/ai_algorithm_engineering_os/20_QUALITY_AUTOMATION/_MOC.md',
]
PLACEHOLDER = re.compile(r'\[(?:FEATURE-ID|PATCH-ID|NNNN|Title|ID)\]')
ALLOWED_PLACEHOLDER_DIRS = {'templates','14_TEMPLATES','08_PROMPT_LIBRARY','16_EXAMPLES'}


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    errors=[]; warnings=[]
    for rel in REQUIRED:
        p=root/rel
        if not p.is_file(): errors.append(f'missing required policy file: {rel}')
        elif not p.read_text(encoding='utf-8',errors='replace').strip(): errors.append(f'empty policy file: {rel}')
    agents=root/'AGENTS.md'
    if agents.is_file():
        text=agents.read_text(encoding='utf-8')
        for phrase in ['Policy precedence','Mandatory Engineering Sequence','Hard Prohibitions','Required Final Report']:
            if phrase not in text: errors.append(f'AGENTS.md missing section: {phrase}')
    seen={}
    for p in root.rglob('*'):
        if not p.is_file() or '.git' in p.parts: continue
        rel=p.relative_to(root).as_posix(); key=rel.lower()
        if key in seen: errors.append(f'case-insensitive duplicate: {seen[key]} / {rel}')
        seen[key]=rel
        if p.suffix.lower()=='.md' and not any(part in ALLOWED_PLACEHOLDER_DIRS for part in p.parts):
            text=p.read_text(encoding='utf-8',errors='replace')
            for m in PLACEHOLDER.finditer(text): warnings.append(f'possible placeholder: {rel}: {m.group(0)}')
    print(f'Root: {root}')
    print(f'Errors: {len(errors)}')
    print(f'Warnings: {len(warnings)}')
    for x in errors[:100]: print('ERROR:',x)
    for x in warnings[:50]: print('WARN :',x)
    return 1 if errors else 0

if __name__=='__main__':
    raise SystemExit(main())
