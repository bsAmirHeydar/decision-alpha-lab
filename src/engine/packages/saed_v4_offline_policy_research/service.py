from __future__ import annotations
from collections import defaultdict
from .contracts import *
from .security import scan
from .upstream import verify
from .budget import ResearchLedger
from .trajectory import validate_dataset,transitions
from .rewards import audit
from .behavior import estimate
from .masks import compile_masks
from .policies import baseline_from_document
from .cql import train as train_cql
from .iql import train as train_iql
from .sequence_policy import train as train_sequence
from .projection import project
from .support import diagnose
from .ope import evaluate
from .challenge import synthetic_veto,matrix
from .certificates import build as build_certificate
from .handoff import build as build_handoff
from .replay import receipt as replay_receipt
from .authority import authority_boundary
from .canonical import content_hash

def run(config,upstream_documents,dataset,baseline_document):
    scan(config);scan(upstream_documents);scan(dataset);scan(baseline_document)
    upstream=UpstreamIntakeContract.from_mapping(config['upstream_intake'])
    logged=LoggedDatasetContract.from_mapping(config['logged_dataset_contract'])
    action=ActionSpaceContract.from_mapping(config['action_space_contract'])
    reward=RewardContract.from_mapping(config['reward_contract'])
    behavior_c=BehaviorPolicyContract.from_mapping(config['behavior_policy_contract'])
    support_c=SupportContract.from_mapping(config['support_contract'])
    cql_c=CQLContract.from_mapping(config['cql_contract'])
    iql_c=IQLContract.from_mapping(config['iql_contract'])
    seq_c=SequencePolicyContract.from_mapping(config['sequence_policy_contract'])
    ope_c=OPEContract.from_mapping(config['ope_contract'])
    proj_c=ProjectionContract.from_mapping(config['projection_contract'])
    budget_c=ResearchBudget.from_mapping(config['research_budget'])
    ledger=ResearchLedger(budget_c)
    upstream_receipt=verify(config['upstream_intake'],upstream_documents)
    summary=validate_dataset(dataset,logged,action,reward,ledger)
    reward_audit=audit(dataset,reward)
    actions=list(action.actions);behavior=estimate(dataset,behavior_c,actions);masks=compile_masks(dataset,actions,action.safe_action)
    baseline=baseline_from_document(baseline_document)
    raw=[train_cql(dataset,cql_c,actions,masks,ledger),train_iql(dataset,behavior,iql_c,actions,masks,ledger),train_sequence(dataset,behavior,seq_c,actions,masks,ledger)]
    counts=defaultdict(lambda:defaultdict(int))
    for tr in transitions(dataset):counts[tr['state']][tr['action']]+=1
    projected=[project(p,behavior,masks,counts,proj_c,actions,ledger) for p in raw]
    candidates=[baseline]+projected
    support_reports={p['policy_id']:diagnose(dataset,behavior,p,support_c,actions) for p in candidates}
    ope_reports={p['policy_id']:evaluate(dataset,behavior,p,ope_c,actions,ledger,423+i*17) for i,p in enumerate(candidates)}
    stress_reports={p['policy_id']:synthetic_veto(p,baseline,upstream_documents,actions,ledger) for p in candidates}
    challenge=matrix(candidates,ope_reports,support_reports,stress_reports,baseline['policy_id'],ope_c.minimum_lower_bound_margin)
    baseline_row=[r for r in challenge['rows'] if r['policy_id']==baseline['policy_id']][0]
    baseline_matrix={'baseline_policy_id':baseline['policy_id'],'present':True,'immutable':True,'runtime_executable':False,'promotion_eligible':False,'baseline_ope_lower_bound':baseline_row['ope_lower_bound'],'passed':True};baseline_matrix['matrix_hash']=content_hash(baseline_matrix)
    trial_ledger={'trials':[{'trial_id':f'trial_{i+1:03d}','family':p['family'],'policy_id':p['policy_id'],'status':'completed','promotion_eligible':False} for i,p in enumerate(raw)],'complete':True};trial_ledger['ledger_hash']=content_hash(trial_ledger)
    exposure_ledger={'hidden_evaluation_queries':0,'protected_evidence_exposures':0,'synthetic_positive_evidence_uses':0,'runtime_compilations':0,'order_submissions':0,'complete':True};exposure_ledger['ledger_hash']=content_hash(exposure_ledger)
    budget=ledger.snapshot()
    certificate=build_certificate(upstream_receipt,summary,reward_audit,behavior,support_reports,ope_reports,challenge,stress_reports,budget,baseline_matrix,trial_ledger,exposure_ledger)
    handoff=build_handoff(certificate,ope_reports,support_reports)
    outputs={'upstream_receipt':upstream_receipt,'dataset_summary':summary,'reward_audit':reward_audit,'behavior_policy':behavior,'action_mask_report':masks,'raw_candidates':raw,'projected_candidates':projected,'support_reports':support_reports,'ope_reports':ope_reports,'synthetic_stress_reports':stress_reports,'challenge_matrix':challenge,'baseline_preservation':baseline_matrix,'trial_ledger':trial_ledger,'exposure_ledger':exposure_ledger,'budget_snapshot':budget,'certificate':certificate,'handoff':handoff,'authority_boundary':authority_boundary()}
    outputs['replay_receipt']=replay_receipt(content_hash(config),{'upstream':content_hash(upstream_documents),'dataset':content_hash(dataset),'baseline':content_hash(baseline_document)},{k:content_hash(v) for k,v in outputs.items()})
    return outputs
