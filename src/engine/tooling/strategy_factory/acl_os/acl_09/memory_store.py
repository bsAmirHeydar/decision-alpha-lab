from __future__ import annotations
from pathlib import Path
from typing import Any
from .canonical import with_digest,stable_id,digest_object
from .io import load_json

def load_prior(root:Path|None)->dict[str,Any]:
    if root is None: return {'memory_fingerprints':{},'proposal_fingerprints':{},'parent_memory_index_digest':'GENESIS','prior_root':None}
    root=root.resolve()
    if not (root/'.acl09_generated_root').is_file(): raise ValueError('ACL09_PRIOR_ROOT_MARKER_MISSING')
    index=load_json(root/'memory/memory_index.json'); portfolio=load_json(root/'planner/plan_portfolio.json')
    fingerprints={x['duplicate_fingerprint']:x['memory_entry_id'] for x in index.get('entries',[])}
    proposals={x['proposal_fingerprint']:x['proposal_id'] for x in portfolio.get('proposals',[]) if x['proposal_status']=='SELECTED_PROPOSAL_NOT_AUTHORIZED'}
    return {'memory_fingerprints':fingerprints,'proposal_fingerprints':proposals,'parent_memory_index_digest':index['memory_index_digest'],'prior_root':root}

def decide_admissions(records:list[dict],equiv:dict,report_id:str,prior:dict)->tuple[list[dict],list[dict],list[dict],list[dict]]:
    byid={r['experience_id']:r for r in records}; decisions=[]; entries=[]; aliases=[]; quarantines=[]
    for cluster in equiv['clusters']:
        members=cluster['member_experience_ids']; rep=byid[cluster['canonical_experience_id']]; fp=cluster['duplicate_fingerprint']; prior_id=prior['memory_fingerprints'].get(fp)
        if prior_id:
            for eid in members:
                r=byid[eid]; decisions.append(_decision(r,'LINKED_PRIOR_DUPLICATE',prior_id,report_id,'EXACT_FINGERPRINT_IN_PRIOR_MEMORY'))
                aliases.append(_alias(r,prior_id,'PRIOR_MEMORY',report_id))
            continue
        if rep['experience_class']=='DIAGNOSTIC_EXCLUSION':
            qid=stable_id('MEMQUAR',report_id,rep['experience_id'])
            for eid in members:
                r=byid[eid]; decisions.append(_decision(r,'QUARANTINED_DIAGNOSTIC',qid,report_id,'DIAGNOSTIC_NON_SELECTABLE'))
            quarantines.append(with_digest({'schema_version':'1.0.0','quarantine_id':qid,'experience_id':rep['experience_id'],'experience_digest':rep['experience_digest'],'duplicate_fingerprint':fp,'reason_codes':['DIAGNOSTIC_LANE_NON_SELECTABLE'],'selectable':False,'planner_eligible':False,'promotion_allowed':False},'quarantine_digest'))
            continue
        entry_id=stable_id('MEMENTRY',report_id,fp)
        entry=with_digest({'schema_version':'1.0.0','memory_entry_id':entry_id,'canonical_experience_id':rep['experience_id'],'canonical_experience_digest':rep['experience_digest'],'duplicate_fingerprint':fp,'experience_class':rep['experience_class'],'knowledge_polarity':rep['knowledge_polarity'],'setup_id':rep['setup_id'],'candidate_id':rep['candidate_id'],'source_decision_digest':rep['source_decision_digest'],'source_candidate_report_digest':rep['source_candidate_report_digest'],'reason_codes':rep['reason_codes'],'failed_gate_ids':rep['failed_gate_ids'],'unknown_gate_ids':rep['unknown_gate_ids'],'bounded_research_questions':rep['bounded_research_questions'],'security_classification':'INTERNAL_RESEARCH','append_only':True,'source_semantics_mutated':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'memory_entry_digest')
        entries.append(entry); decisions.append(_decision(rep,'ADMITTED_NEW',entry_id,report_id,'CANONICAL_FINGERPRINT_ADMITTED'))
        for eid in members[1:]:
            r=byid[eid]; decisions.append(_decision(r,'LINKED_BATCH_DUPLICATE',entry_id,report_id,'EXACT_FINGERPRINT_IN_BATCH'))
            aliases.append(_alias(r,entry_id,'CURRENT_BATCH',report_id))
    return sorted(decisions,key=lambda x:x['experience_id']),sorted(entries,key=lambda x:x['memory_entry_id']),sorted(aliases,key=lambda x:x['alias_id']),sorted(quarantines,key=lambda x:x['quarantine_id'])

def _decision(r,status,target,report_id,reason):
    return with_digest({'schema_version':'1.0.0','admission_decision_id':stable_id('MEMADM',report_id,r['experience_id']),'experience_id':r['experience_id'],'experience_digest':r['experience_digest'],'setup_id':r['setup_id'],'admission_status':status,'target_memory_identity':target,'reason_codes':[reason],'source_decision_digest':r['source_decision_digest'],'source_semantics_mutated':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'admission_decision_digest')
def _alias(r,target,scope,report_id):
    return with_digest({'schema_version':'1.0.0','alias_id':stable_id('MEMALIAS',report_id,r['experience_id']),'experience_id':r['experience_id'],'experience_digest':r['experience_digest'],'target_memory_entry_id':target,'duplicate_scope':scope,'source_semantics_mutated':False},'alias_digest')
def build_index(memory_run_id:str,report_id:str,entries:list[dict],aliases:list[dict],quarantines:list[dict],decisions:list[dict],parent_digest:str)->dict:
    return with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'report_id':report_id,'parent_memory_index_digest':parent_digest,'entry_count':len(entries),'alias_count':len(aliases),'quarantine_count':len(quarantines),'decision_count':len(decisions),'entries':[{'memory_entry_id':x['memory_entry_id'],'memory_entry_digest':x['memory_entry_digest'],'duplicate_fingerprint':x['duplicate_fingerprint'],'experience_class':x['experience_class']} for x in entries],'aliases':[{'alias_id':x['alias_id'],'alias_digest':x['alias_digest'],'target_memory_entry_id':x['target_memory_entry_id']} for x in aliases],'quarantines':[{'quarantine_id':x['quarantine_id'],'quarantine_digest':x['quarantine_digest']} for x in quarantines],'append_only':True,'history_rewritten':False},'memory_index_digest')
