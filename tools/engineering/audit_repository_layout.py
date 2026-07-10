#!/usr/bin/env python3
"""Audit expected Decision Alpha Lab repository stage directories."""
from pathlib import Path
import sys

EXPECTED=[
 'docs','lab/01_observation','lab/02_hypotheses','lab/03_experiments','lab/04_analysis',
 'lab/05_validation','lab/06_production','lab/07_monitoring','lab/08_archive',
 'lab/09_execution','lab/10_infrastructure','registry','data'
]

def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); missing=[]
 for rel in EXPECTED:
  if not (root/rel).is_dir(): missing.append(rel)
 print(f'Root: {root}')
 print(f'Missing expected directories: {len(missing)}')
 for rel in missing: print('MISSING:',rel)
 return 1 if missing else 0

if __name__=='__main__': raise SystemExit(main())
