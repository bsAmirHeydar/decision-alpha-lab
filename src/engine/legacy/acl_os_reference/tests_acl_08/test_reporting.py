import json
from src.engine.tooling.strategy_factory.acl_os.acl_08.service import ACL08ReportingExperienceService

def build(acl07_root,permit,policy,tmp_path):
 d=tmp_path/'out'; ACL08ReportingExperienceService().build(acl07_root,permit,policy,d,'2026-07-18T01:00:00Z'); return d
def test_batch_report_counts(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); x=json.loads((d/'reports/batch_report.json').read_text()); assert x['decision_counts']=={'BASELINE_REFERENCE_ONLY':4,'DIAGNOSTIC_EXCLUDED':1,'EVIDENCE_INSUFFICIENT':7}
def test_no_reporting_eligible(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); assert json.loads((d/'reports/batch_report.json').read_text())['reporting_eligible_count']==0
def test_candidate_decisions_preserved(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); upstream=json.loads((acl07_root/'decisions/validation_decision_bundle.json').read_text()); got={json.loads(p.read_text())['setup_id']:json.loads(p.read_text()) for p in (d/'reports/candidates').glob('*.json')}; assert all(got[x['setup_id']]['decision_status']==x['decision_status'] and got[x['setup_id']]['reason_codes']==x['reason_codes'] for x in upstream['decisions'])
def test_executive_has_no_candidate_ids(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); text=(d/'reports/executive_summary.json').read_text(); assert 'SETUP_' not in text and 'CAND_' not in text
def test_external_view_redacted(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); text=(d/'views/external_restricted.json').read_text(); assert not any(x in text for x in ['SETUP_','CAND_','VALDEC_','candidate_id','setup_id'])
def test_internal_view_contains_full_candidates(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); x=json.loads((d/'views/internal_research.json').read_text()); assert len(x['candidate_reports'])==12

def test_baseline_count_excludes_diagnostic_origin(acl07_root,permit,policy,tmp_path):
 d=build(acl07_root,permit,policy,tmp_path); x=json.loads((d/'reports/batch_report.json').read_text()); assert x['baseline_count']==4 and x['diagnostic_count']==1
