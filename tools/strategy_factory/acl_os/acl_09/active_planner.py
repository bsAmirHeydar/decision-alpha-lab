from __future__ import annotations
from .canonical import with_digest,stable_id,digest_object
from .question_registry import by_id

def build_proposals(memory_run_id:str,entries:list[dict],registry:dict,policy:dict,prior_proposals:dict[str,str])->tuple[list[dict],dict,dict]:
    qreg=by_id(registry); sources={}
    for entry in entries:
        if entry['experience_class'] not in {'INSUFFICIENT_EVIDENCE','NEGATIVE_VALIDATION','REPORTABLE_EVIDENCE'}: continue
        for q in entry['bounded_research_questions']:
            if q in qreg: sources.setdefault(q,[]).append(entry)
    evaluated=[]
    for qid,rows in sorted(sources.items()):
        meta=qreg[qid]; src=sorted(x['memory_entry_id'] for x in rows)
        fp=digest_object({'question_id':qid,'source_duplicate_fingerprints':sorted(x['duplicate_fingerprint'] for x in rows),'target_gate':meta['target_gate']})
        score=4*meta['decision_relevance']+3*meta['information_gain']+2*meta['risk_reduction']-meta['cost_units']
        prior_id=prior_proposals.get(fp)
        evaluated.append({'question_id':qid,'target_gate':meta['target_gate'],'source_memory_entry_ids':src,'source_count':len(src),'proposal_fingerprint':fp,'cost_units':meta['cost_units'],'priority_score':score,'information_gain':meta['information_gain'],'risk_reduction':meta['risk_reduction'],'decision_relevance':meta['decision_relevance'],'requires_new_batch':meta['requires_new_batch'],'requires_human_approval':meta['requires_human_approval'],'prior_proposal_id':prior_id})
    evaluated.sort(key=lambda x:(x['prior_proposal_id'] is not None,-x['priority_score'],x['cost_units'],x['question_id']))
    selected=0; cost=0; proposals=[]; suppressed=[]
    for row in evaluated:
        if row['prior_proposal_id']:
            status='SUPPRESSED_DUPLICATE'; reason=['PROPOSAL_ALREADY_EXISTS_IN_PRIOR_MEMORY']; suppressed.append(row['question_id'])
        elif selected>=policy['max_selected_proposals'] or cost+row['cost_units']>policy['max_total_cost_units']:
            status='DEFERRED_BUDGET'; reason=['PLANNER_BUDGET_OR_COUNT_CAP_REACHED']
        else:
            status='SELECTED_PROPOSAL_NOT_AUTHORIZED'; reason=['HIGHEST_BOUNDED_INFORMATION_VALUE_WITHIN_POLICY']; selected+=1; cost+=row['cost_units']
        body={'schema_version':'1.0.0','proposal_id':stable_id('PLAN09',memory_run_id,row['proposal_fingerprint']),'question_id':row['question_id'],'target_gate':row['target_gate'],'source_memory_entry_ids':row['source_memory_entry_ids'],'source_count':row['source_count'],'proposal_fingerprint':row['proposal_fingerprint'],'proposal_status':status,'reason_codes':reason,'priority_score':row['priority_score'],'estimated_cost_units':row['cost_units'],'information_gain_units':row['information_gain'],'risk_reduction_units':row['risk_reduction'],'decision_relevance_units':row['decision_relevance'],'requires_new_frozen_batch':row['requires_new_batch'],'requires_human_approval':row['requires_human_approval'],'research_execution_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
        proposals.append(with_digest(body,'proposal_digest'))
    portfolio=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'policy_id':policy['policy_id'],'proposal_count':len(proposals),'selected_count':sum(x['proposal_status']=='SELECTED_PROPOSAL_NOT_AUTHORIZED' for x in proposals),'deferred_count':sum(x['proposal_status']=='DEFERRED_BUDGET' for x in proposals),'suppressed_count':sum(x['proposal_status']=='SUPPRESSED_DUPLICATE' for x in proposals),'selected_cost_units':sum(x['estimated_cost_units'] for x in proposals if x['proposal_status']=='SELECTED_PROPOSAL_NOT_AUTHORIZED'),'max_selected_proposals':policy['max_selected_proposals'],'max_total_cost_units':policy['max_total_cost_units'],'proposals':[{'proposal_id':x['proposal_id'],'proposal_digest':x['proposal_digest'],'question_id':x['question_id'],'proposal_status':x['proposal_status'],'proposal_fingerprint':x['proposal_fingerprint']} for x in proposals],'research_execution_allowed':False,'automatic_scheduling_allowed':False},'portfolio_digest')
    budget=with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'selected_count':portfolio['selected_count'],'selected_cost_units':portfolio['selected_cost_units'],'remaining_proposal_slots':policy['max_selected_proposals']-portfolio['selected_count'],'remaining_cost_units':policy['max_total_cost_units']-portfolio['selected_cost_units'],'budget_expansion_allowed':False,'passed':portfolio['selected_count']<=policy['max_selected_proposals'] and portfolio['selected_cost_units']<=policy['max_total_cost_units']},'budget_report_digest')
    return proposals,portfolio,budget
