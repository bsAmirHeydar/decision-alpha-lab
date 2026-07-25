from __future__ import annotations
import json,shutil,tempfile
from collections import Counter
from pathlib import Path
from typing import Any
from .artifact_manifest import build_output_manifest
from .authority import validate_authority
from .canonical import digest_object,stable_id,with_digest
from .decision_engine import decide
from .event_ledger import build_event_ledger,verify_event_ledger
from .gate_engine import preliminary,replace_family_gates
from .gate_registry import registry_snapshot,validate_registry
from .handoff_input import load_acl06_bundle
from .io import atomic_publish,dump_json
from .obsidian_projection import summary_md,candidate_index_md
from .policies import CLAIM_CEILING,VALIDATOR_VERSION
from .provenance import build_provenance
from .statistics import benjamini_hochberg,binomial_upper_tail
from .validation_policy import validate_policy

class ACL07UnifiedValidationService:
    def validate(self,acl06_root:Path,permit:dict[str,Any],policy:dict[str,Any],destination:Path,validated_at:str)->dict[str,Any]:
        bundle=load_acl06_bundle(acl06_root); authority=validate_authority(permit,bundle['handoff']); policy=validate_policy(policy); registry=validate_registry(registry_snapshot())
        validation_id=stable_id('VALIDATION',bundle['handoff']['run_id'],bundle['handoff']['handoff_digest'],policy['policy_digest'],validated_at,length=32)
        destination=destination.resolve(); staging=Path(tempfile.mkdtemp(prefix='.acl07_staging_',dir=destination.parent if destination.parent.exists() else None))
        try:
            (staging/'.acl07_generated_root').write_text('ACL-07 GENERATED ROOT — DO NOT HAND EDIT\n',encoding='utf-8')
            binding=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'acl06_handoff_digest':bundle['handoff']['handoff_digest'],'acl06_result_bundle_digest':bundle['bundle']['result_bundle_digest'],'acl06_input_bundle_digest':bundle['bundle_digest'],'research_results_mutated':False},'binding_digest')
            dump_json(staging/'binding/acl06_binding.json',binding); dump_json(staging/'authority/authority_report.json',authority); dump_json(staging/'policy/validation_policy_snapshot.json',policy); dump_json(staging/'policy/gate_registry_snapshot.json',registry)
            candidates=[dict(c) for c in bundle['candidates']]
            gates_by_setup={}; pvals=[]
            for c in candidates:
                seg=bundle['segments_by_setup'][c['setup_id']]; c['_test_accuracy']=seg['TEST']['accuracy']
                gates=preliminary(c,seg,policy,bundle['bundle_digest']); gates_by_setup[c['setup_id']]=gates
                if c['lane']=='RESEARCH': pvals.append((c['setup_id'],binomial_upper_tail(c['correct'],c['signals'])))
            qvals=benjamini_hochberg(pvals)
            baseline_test=[c['_test_accuracy'] for c in candidates if c['lane']=='RESEARCH' and c['origin']=='BASELINE' and c['_test_accuracy'] is not None]
            best_baseline=max(baseline_test) if baseline_test else None
            gate_docs=[]; decisions=[]
            for c in candidates:
                replace_family_gates(gates_by_setup[c['setup_id']],c,qvals.get(c['setup_id']),best_baseline,policy)
                gbody={'schema_version':'1.0.0','validation_id':validation_id,'setup_id':c['setup_id'],'candidate_id':c['candidate_id'],'lane':c['lane'],'origin':c['origin'],'gates':[gates_by_setup[c['setup_id']][x] for x in registry_order(registry)]}
                gdoc=with_digest(gbody,'candidate_gate_digest'); gate_docs.append(gdoc); dump_json(staging/f"gates/candidates/{c['setup_id']}.json",gdoc)
                d=decide(c,gates_by_setup[c['setup_id']]); decisions.append(d); dump_json(staging/f"decisions/candidates/{c['setup_id']}.json",d)
            matrix=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'candidate_count':len(gate_docs),'gate_count_per_candidate':len(registry['entries']),'candidate_gate_digests':[x['candidate_gate_digest'] for x in gate_docs],'gate_order':registry_order(registry)},'gate_matrix_digest')
            dump_json(staging/'gates/gate_matrix.json',matrix)
            mt=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'method':'BENJAMINI_HOCHBERG','family_size':len(pvals),'maximum_fdr_q':policy['thresholds']['maximum_fdr_q'],'q_values':qvals,'diagnostic_candidates_excluded':True},'report_digest'); dump_json(staging/'reports/multiple_testing_report.json',mt)
            di=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'diagnostic_count':sum(c['lane']=='DIAGNOSTIC' for c in candidates),'diagnostic_selectable':False,'diagnostic_promoted':False,'passed':True},'report_digest'); dump_json(staging/'reports/diagnostic_isolation_report.json',di)
            integrity=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'acl06_bundle_verified':True,'candidate_files_verified':len(candidates),'segment_results_verified':sum(len(x) for x in bundle['segments_by_setup'].values()),'research_results_mutated':False,'passed':True},'report_digest'); dump_json(staging/'reports/integrity_report.json',integrity)
            sec=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'network_access_allowed':False,'secret_access_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'promotion_authority_granted':False,'passed':True},'report_digest'); dump_json(staging/'reports/security_boundary_report.json',sec)
            counts=dict(Counter(d['decision_status'] for d in decisions))
            db=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'candidate_count':len(decisions),'decision_counts':counts,'decisions':decisions,'claim_ceiling':CLAIM_CEILING,'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'decision_bundle_digest')
            dump_json(staging/'decisions/validation_decision_bundle.json',db)
            validation=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'state':'COMPLETED_NON_PROMOTIONAL','validated_at':validated_at,'validator_version':VALIDATOR_VERSION,'claim_ceiling':CLAIM_CEILING,'input_binding_digest':binding['binding_digest'],'policy_digest':policy['policy_digest'],'gate_registry_digest':registry['registry_digest'],'gate_matrix_digest':matrix['gate_matrix_digest'],'decision_bundle_digest':db['decision_bundle_digest'],'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'validation_run_digest')
            dump_json(staging/'validation/validation_run.json',validation)
            events=[('ACL06_EVIDENCE_ACCEPTED',{'binding_digest':binding['binding_digest']}),('VALIDATION_POLICY_BOUND',{'policy_digest':policy['policy_digest']}),('UNIFIED_GATES_APPLIED',{'gate_matrix_digest':matrix['gate_matrix_digest']}),('NON_PROMOTIONAL_DECISIONS_ISSUED',{'decision_bundle_digest':db['decision_bundle_digest']}),('VALIDATION_COMPLETED',{'validation_run_digest':validation['validation_run_digest']})]
            ledger=build_event_ledger(validation_id,events,validated_at)
            if not verify_event_ledger(ledger): raise RuntimeError('event ledger failed self-check')
            dump_json(staging/'events/validation_event_ledger.json',ledger)
            prov=build_provenance(validation_id,bundle,policy,matrix,db,ledger); dump_json(staging/'lineage/validation_provenance_graph.json',prov)
            handoff=with_digest({'schema_version':'1.0.0','handoff_type':'ACL07_TO_ACL08','validation_id':validation_id,'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'claim_ceiling':CLAIM_CEILING,'validation_run_digest':validation['validation_run_digest'],'decision_bundle_digest':db['decision_bundle_digest'],'gate_matrix_digest':matrix['gate_matrix_digest'],'event_ledger_digest':ledger['ledger_digest'],'provenance_graph_digest':prov['graph_digest'],'required_acl08_actions':['BUILD_BATCH_REPORT','PROJECT_VALIDATION_EVIDENCE','CAPTURE_NON_PROMOTIONAL_EXPERIENCE'],'forbidden_acl08_actions':['MUTATE_VALIDATION_DECISIONS','INFER_ALPHA_FROM_REPORTING','PROMOTE_DIAGNOSTIC_LANE','AUTHORIZE_EXECUTION','ACTIVATE_CAPITAL'],'alpha_claim_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'handoff_digest')
            dump_json(staging/'handoff/acl08_handoff.json',handoff)
            (staging/'docs').mkdir(parents=True,exist_ok=True); (staging/'docs/ACL07_VALIDATION_SUMMARY.md').write_text(summary_md(validation,db),encoding='utf-8',newline='\n'); (staging/'docs/CANDIDATE_DECISION_INDEX.md').write_text(candidate_index_md(db),encoding='utf-8',newline='\n')
            manifest=build_output_manifest(staging,validation_id); dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','validation_id':validation_id,'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'validator_version':VALIDATOR_VERSION,'claim_ceiling':CLAIM_CEILING,'validation_run_digest':validation['validation_run_digest'],'decision_bundle_digest':db['decision_bundle_digest'],'gate_matrix_digest':matrix['gate_matrix_digest'],'event_ledger_digest':ledger['ledger_digest'],'acl08_handoff_digest':handoff['handoff_digest'],'output_manifest_digest':manifest['manifest_digest'],'live_order_submission_allowed':False,'capital_activation_allowed':False},'receipt_digest')
            dump_json(staging/'validation_receipt.json',receipt)
            atomic_publish(staging,destination)
            return {'validation_id':validation_id,'decision_counts':counts,'handoff_digest':handoff['handoff_digest'],'destination':str(destination)}
        except Exception:
            if staging.exists(): shutil.rmtree(staging,ignore_errors=True)
            raise

def registry_order(registry:dict[str,Any])->list[str]: return [x['gate_id'] for x in sorted(registry['entries'],key=lambda x:x['order'])]
