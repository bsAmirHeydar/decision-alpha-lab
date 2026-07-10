#!/usr/bin/env python3
"""Scaffold a Decision Alpha Lab work packet.

Usage: python tools/engineering/new_alpha_lab_packet.py KIND ID "Title" [output-root]
KIND: feature | bug | experiment | hotfix
"""
from __future__ import annotations
from pathlib import Path
from datetime import date
import re, shutil, sys

FILES={
 'feature':['FEATURE_PACKET.md','PATCH_MANIFEST.md','ADR.md'],
 'bug':['PATCH_MANIFEST.md','ADR.md'],
 'experiment':['EXPERIMENT_PACKET.md','DATASET_CONTRACT.md','ADR.md'],
 'hotfix':['PATCH_MANIFEST.md','ADR.md'],
}

def slug(s): return re.sub(r'[^A-Za-z0-9._-]+','-',s).strip('-').lower()

def main():
 if len(sys.argv)<4:
  print(__doc__); return 2
 kind,ident,title=sys.argv[1],sys.argv[2],sys.argv[3]
 if kind not in FILES: print('ERROR: invalid KIND'); return 2
 root=Path(sys.argv[4] if len(sys.argv)>4 else '.').resolve()
 repo=Path(__file__).resolve().parents[2]
 templates=repo/'docs'/'engineering'/'templates'
 target=root/f'{slug(ident)}-{slug(title)}'
 if target.exists(): print(f'ERROR: target exists: {target}'); return 1
 target.mkdir(parents=True)
 for name in FILES[kind]:
  text=(templates/name).read_text(encoding='utf-8')
  text=text.replace('[FEATURE-ID]',ident).replace('[PATCH-ID]',ident).replace('[ID]',ident)
  text=text.replace('[Title]',title).replace('[NNNN]',ident)
  (target/name).write_text(text,encoding='utf-8',newline='\n')
 (target/'README.md').write_text(f'# {ident} — {title}\n\nKind: {kind}\nCreated: {date.today().isoformat()}\n',encoding='utf-8')
 print(target); return 0

if __name__=='__main__': raise SystemExit(main())
