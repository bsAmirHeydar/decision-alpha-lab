import json
from tools.strategy_factory.acl_os.acl_09.service import ACL09MemoryPlannerService

def build(acl08_root,permit,memory_policy,planner_policy,tmp_path,prior=None):
 d=tmp_path/'out'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,d,'2026-07-18T02:00:00Z',prior); return d

def test_reference_admission_counts(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); x=json.loads((d/'memory/memory_index.json').read_text()); assert (x['entry_count'],x['alias_count'],x['quarantine_count'],x['decision_count'])==(5,6,1,12)
def test_exact_duplicates_detected(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); x=json.loads((d/'duplicates/equivalence_report.json').read_text()); assert x['unique_fingerprint_count']==6 and x['exact_duplicate_count']==6
def test_near_equivalence_not_auto_merged(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); x=json.loads((d/'duplicates/equivalence_report.json').read_text()); assert x['near_equivalence_count']>=1 and all(not p['auto_merge_allowed'] for p in x['near_equivalences'])
def test_diagnostic_quarantined(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); q=list((d/'memory/quarantine').glob('*.json')); assert len(q)==1 and json.loads(q[0].read_text())['selectable'] is False
def test_source_decision_digests_preserved(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); assert all(json.loads(p.read_text())['source_decision_digest'].startswith('sha256:') for p in (d/'memory/entries').glob('*.json'))
def test_second_ingestion_links_prior(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 first=tmp_path/'first'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,first,'2026-07-18T02:00:00Z'); second=tmp_path/'second'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,second,'2026-07-18T03:00:00Z',first); x=json.loads((second/'memory/memory_index.json').read_text()); assert x['entry_count']==0 and x['alias_count']==11 and x['quarantine_count']==1
