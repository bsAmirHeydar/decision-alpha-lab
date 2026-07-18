import json
from tools.strategy_factory.acl_os.acl_08.service import ACL08ReportingExperienceService

def run(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z'); return d
def test_experience_counts(acl07_root,permit,policy,tmp_path):
 d=run(acl07_root,permit,policy,tmp_path); x=json.loads((d/'experience/experience_bundle.json').read_text()); assert x['experience_counts']=={'BASELINE_REFERENCE':4,'DIAGNOSTIC_EXCLUSION':1,'INSUFFICIENT_EVIDENCE':7}
def test_records_are_non_promotional(acl07_root,permit,policy,tmp_path):
 d=run(acl07_root,permit,policy,tmp_path); assert all(json.loads(p.read_text())['promotion_allowed'] is False for p in (d/'experience/records').glob('*.json'))
def test_memory_not_ingested_in_acl08(acl07_root,permit,policy,tmp_path):
 d=run(acl07_root,permit,policy,tmp_path); x=json.loads((d/'experience/experience_bundle.json').read_text()); assert x['memory_ingestion_status']=='NOT_INGESTED' and x['active_planning_status']=='NOT_RUN'
def test_unknown_evidence_separated_from_negative(acl07_root,permit,policy,tmp_path):
 d=run(acl07_root,permit,policy,tmp_path); u=json.loads((d/'experience/unknown_evidence.json').read_text()); n=json.loads((d/'experience/negative_knowledge.json').read_text()); assert u['record_count']==12 and n['record_count']==0 and n['absence_of_negative_records_does_not_imply_alpha']
def test_diagnostic_record_non_selectable(acl07_root,permit,policy,tmp_path):
 d=run(acl07_root,permit,policy,tmp_path); rows=[json.loads(p.read_text()) for p in (d/'experience/records').glob('*.json')]; r=next(x for x in rows if x['experience_class']=='DIAGNOSTIC_EXCLUSION'); assert r['knowledge_polarity']=='NON_SELECTABLE_DIAGNOSTIC' and r['promotion_allowed'] is False
def test_duplicate_fingerprint_deterministic(acl07_root,permit,policy,tmp_path):
 a=run(acl07_root,permit,policy,tmp_path/'a'); b=run(acl07_root,permit,policy,tmp_path/'b'); aa=sorted(json.loads(p.read_text())['duplicate_fingerprint'] for p in (a/'experience/records').glob('*.json')); bb=sorted(json.loads(p.read_text())['duplicate_fingerprint'] for p in (b/'experience/records').glob('*.json')); assert aa==bb
