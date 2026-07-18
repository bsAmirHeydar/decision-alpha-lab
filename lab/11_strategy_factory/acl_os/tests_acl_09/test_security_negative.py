import copy,json,shutil,pytest
from tools.strategy_factory.acl_os.acl_09.replay_validator import verify_generated_root
from tools.strategy_factory.acl_os.acl_09.service import ACL09MemoryPlannerService

def build(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=tmp_path/'out'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,d,'2026-07-18T02:00:00Z'); return d
def test_manifest_detects_tamper(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); p=d/'memory/memory_index.json'; p.write_text(p.read_text()+' '); assert not verify_generated_root(d)['passed']
def test_poisoned_input_rejected(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=tmp_path/'acl08'; shutil.copytree(acl08_root,d); p=next((d/'experience/records').glob('*.json')); x=json.loads(p.read_text()); x['bounded_research_questions'].append('ACTIVATE_CAPITAL'); from tools.strategy_factory.acl_os.acl_08.canonical import digest_object; x['experience_digest']=digest_object({k:v for k,v in x.items() if k!='experience_digest'}); p.write_text(json.dumps(x));
 with pytest.raises(Exception): ACL09MemoryPlannerService().build(d,permit,memory_policy,planner_policy,tmp_path/'out','2026-07-18T02:00:00Z')
def test_security_report_denies_all_authority(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); x=json.loads((d/'security/security_boundary_report.json').read_text()); assert not x['research_execution_allowed'] and not x['promotion_allowed'] and not x['live_order_submission_allowed'] and not x['capital_activation_allowed'] and not x['doctrine_amendment_allowed']
def test_generated_docs_do_not_claim_alpha(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); text=(d/'docs/ACL09_MEMORY_AND_PLANNER_SUMMARY.md').read_text().lower(); assert 'no alpha' in text and 'capital authority' in text
def test_diagnostic_not_in_memory_entries(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); assert all(json.loads(p.read_text())['experience_class']!='DIAGNOSTIC_EXCLUSION' for p in (d/'memory/entries').glob('*.json'))
