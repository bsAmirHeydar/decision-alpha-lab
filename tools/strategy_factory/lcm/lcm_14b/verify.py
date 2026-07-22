from __future__ import annotations
from pathlib import Path
from .canonical import file_digest, verify_embedded_digest
from .io import load_json, iter_jsonl
from .constants import PHASE_ID, CLAIM_CEILING
REQUIRED=(
'quarantine_registry.json','observation_registry.json','restoration_drill_registry.json','retirement_eligibility_registry.json','active_path_exclusion_registry.json','observation_report.json','quarantine_observation_receipt.json','rollback_manifest.json','LCM14B_TO_LCM15A_HANDOFF.json','residual_retirement_risk.md','records/quarantine_package_records.jsonl','records/observation_cycle_records.jsonl','records/active_reference_records.jsonl','records/restoration_drill_records.jsonl','records/retirement_eligibility_records.jsonl','observation_ledger.jsonl','reports/acceptance_report.json','reports/hostile_review_report.json','output_manifest.json')
DIGESTS={'quarantine_registry.json':'registry_digest','observation_registry.json':'registry_digest','restoration_drill_registry.json':'registry_digest','retirement_eligibility_registry.json':'registry_digest','active_path_exclusion_registry.json':'registry_digest','observation_report.json':'report_digest','quarantine_observation_receipt.json':'receipt_digest','rollback_manifest.json':'rollback_manifest_digest','LCM14B_TO_LCM15A_HANDOFF.json':'handoff_digest','reports/acceptance_report.json':'report_digest','reports/hostile_review_report.json':'report_digest','output_manifest.json':'output_manifest_digest'}
def verify_package(root: Path)->list[str]:
 e=[]
 for r in REQUIRED:
  if not (root/r).is_file(): e.append('MISSING:'+r)
 if e:return e
 vals={}
 for fn,field in DIGESTS.items():
  v=load_json(root/fn); vals[fn]=v
  if v.get('phase_id')!=PHASE_ID:e.append('PHASE:'+fn)
  if v.get('claim_ceiling')!=CLAIM_CEILING:e.append('CLAIM:'+fn)
  if v.get('validation_status')!='PASS':e.append('STATUS:'+fn)
  if not verify_embedded_digest(v,field):e.append('DIGEST:'+fn)
 pk=list(iter_jsonl(root/'records/quarantine_package_records.jsonl')); ob=list(iter_jsonl(root/'records/observation_cycle_records.jsonl')); rr=list(iter_jsonl(root/'records/restoration_drill_records.jsonl')); el=list(iter_jsonl(root/'records/retirement_eligibility_records.jsonl'))
 if len(pk)!=136:e.append('PACKAGE_COUNT')
 if len(ob)!=272:e.append('OBSERVATION_COUNT')
 if len(rr)!=136 or any(x.get('result')!='PASS' for x in rr):e.append('RESTORATION')
 if len(el)!=136:e.append('ELIGIBILITY_COUNT')
 if any(x.get('deletion_approved') or x.get('deletion_authorized') for x in el):e.append('DELETION_AUTHORITY')
 if any(x.get('external_consumer_evidence_state')!='UNKNOWN_BLOCKING_DELETION_APPROVAL' for x in el):e.append('EXTERNAL_UNKNOWN')
 if vals['retirement_eligibility_registry.json'].get('proof_eligible_count')!=136:e.append('PROOF_ELIGIBLE')
 if vals['retirement_eligibility_registry.json'].get('deletion_approved_count')!=0:e.append('DELETION_APPROVED')
 if vals['quarantine_observation_receipt.json'].get('active_source_blocked_count')!=477:e.append('ACTIVE_SOURCE_BLOCKED')
 for row in pk:
  p=root/row['quarantine_payload_path']
  if not p.is_file() or file_digest(p)!=row['original_bytes_sha256']:e.append('PAYLOAD:'+row['consumer_id'])
  for key in ('manifest_path','immutability_contract_path','restoration_report_path'):
   if not (root/row[key]).is_file():e.append('PACKAGE_FILE:'+row['consumer_id']+':'+key)
 out=vals['output_manifest.json']; listed=set()
 for item in out.get('files',[]):
  listed.add(item['path']); p=root/item['path']
  if not p.is_file() or file_digest(p)!=item['sha256']:e.append('OUTPUT_HASH:'+item['path'])
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='output_manifest.json'}
 if listed!=actual:e.append('OUTPUT_COVERAGE')
 if out.get('file_count')!=len(listed):e.append('OUTPUT_COUNT')
 return e
