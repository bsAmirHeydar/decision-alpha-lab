#!/usr/bin/env python3
from __future__ import annotations
from tools.repository_paths import find_repository_root
import json, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker
ROOT=find_repository_root(__file__)
S=ROOT/'schemas/legacy/strategy_factory/saed_v4_00'; E=ROOT/'examples/legacy/strategy_factory/saed_v4_00'
MAPPING={
'research_constitution':'research_constitution.yaml','authority_matrix':'authority_matrix.yaml','evidence_role_policy':'evidence_role_policy.yaml','objective_policy':'objective_policy.yaml','baseline_policy':'baseline_policy.yaml','program_manifest':'program_manifest.json','crosswalk':'ucee_i01_i18_crosswalk.json','exposure_budget':'exposure_budget.json','external_evidence_claim':'external_static_evidence_claim.json','handoff':'phase_handoff_v4_00_to_v4_01.json'}
errors=[]
for path in sorted(S.glob('*.schema.json')):
 try: Draft202012Validator.check_schema(json.loads(path.read_text(encoding='utf-8')))
 except Exception as exc: errors.append(f'{path.relative_to(ROOT)}: schema: {exc}')
for name,docname in MAPPING.items():
 schema=json.loads((S/f'{name}.schema.json').read_text(encoding='utf-8'))
 p=E/docname; doc=yaml.safe_load(p.read_text(encoding='utf-8')) if p.suffix in {'.yaml','.yml'} else json.loads(p.read_text(encoding='utf-8'))
 for err in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(doc):
  errors.append(f'{p.relative_to(ROOT)}: {list(err.absolute_path)}: {err.message}')
print(json.dumps({'status':'pass' if not errors else 'fail','schema_count':len(list(S.glob('*.schema.json'))),'validated_examples':len(MAPPING),'errors':errors},indent=2))
raise SystemExit(0 if not errors else 1)
