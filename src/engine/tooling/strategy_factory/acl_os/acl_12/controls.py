from __future__ import annotations
from .canonical import stable_id,with_digest
from .policies import CONTROL_STATUSES
REFERENCE_SATISFIED={'INPUT_PACKAGE_INTEGRITY','IDENTITY_AND_LINEAGE_BINDING','LEAST_PRIVILEGE_CAPABILITIES','NETWORK_EGRESS_DENY','SECRET_MATERIAL_ABSENCE','PRODUCTION_KEY_ACCESS_DENY','SIGNING_CUSTODY_INTERFACE','SUPPLY_CHAIN_INVENTORY','REFERENCE_SBOM','DEPENDENCY_RECALL_GRAPH','STATIC_CODE_SCAN','SECRET_SCAN','MQL5_FORBIDDEN_API_SCAN','PATH_TRAVERSAL_DEFENSE','SYMLINK_SUBSTITUTION_DEFENSE','RUNTIME_TCB_MINIMIZATION','PLUGIN_CAPABILITY_SANDBOX','AUDIT_HASH_CHAIN','NON_REPUDIATION_INTERFACE','OPERATOR_SEPARATION','INCIDENT_RESPONSE_PLAYBOOK','REVOCATION_AND_QUARANTINE','DATA_CLASSIFICATION','BROKER_AND_CAPITAL_ISOLATION','KILL_SWITCH_AND_SAFE_SHUTDOWN'}
EXTERNAL_UNKNOWN={'REPRODUCIBLE_BUILD_EVIDENCE','PRIVILEGED_WORKSTATION_ASSURANCE','INCIDENT_TABLETOP_EVIDENCE','BACKUP_RECOVERY_TEST','SECURITY_MONITORING_INTEGRATION','RED_TEAM_VALIDATION','ARTIFACT_ENCRYPTION_AND_KEY_ROTATION','CI_BRANCH_PROTECTION'}
def _r(control:dict,status:str,reason:str,evidence:list[str])->dict:
    assert status in CONTROL_STATUSES
    return with_digest({'schema_version':'1.0.0','control_id':control['control_id'],'status':status,'reason_code':reason,'evidence_refs':sorted(set(evidence)),'blocks_production':control['blocks_production'],'unknown_blocks_production':True},'result_digest')
def assess_controls(bundle:dict,registry:dict,artifacts:dict,assessed_at:str)->dict:
    common=[bundle['binding']['binding_digest'],bundle['decision']['custody_decision_digest']]
    evidence={
      'SECRET_SCAN':[artifacts['secret_scan']['scan_digest']], 'STATIC_CODE_SCAN':[artifacts['static_scan']['scan_digest']], 'MQL5_FORBIDDEN_API_SCAN':[artifacts['mql5_scan']['scan_digest']], 'PATH_TRAVERSAL_DEFENSE':[artifacts['path_scan']['scan_digest']], 'SYMLINK_SUBSTITUTION_DEFENSE':[artifacts['path_scan']['scan_digest']], 'REFERENCE_SBOM':[artifacts['sbom']['sbom_digest']], 'SUPPLY_CHAIN_INVENTORY':[artifacts['sbom']['sbom_digest']], 'DEPENDENCY_RECALL_GRAPH':[artifacts['recall']['graph_digest']], 'OPERATOR_SEPARATION':[artifacts['operator']['matrix_digest']], 'SIGNING_CUSTODY_INTERFACE':[artifacts['key_custody']['interface_digest']], 'INCIDENT_RESPONSE_PLAYBOOK':[artifacts['incident']['readiness_digest']], 'REVOCATION_AND_QUARANTINE':[artifacts['revocation']['plan_digest']]}
    results=[]
    for c in registry['controls']:
        cid=c['control_id']
        if cid in REFERENCE_SATISFIED:
            status='SATISFIED_REFERENCE'; reason='REFERENCE_CONTROL_EVIDENCE_VERIFIED'
        elif cid in EXTERNAL_UNKNOWN:
            status='UNKNOWN'; reason='PRODUCTION_OR_EXTERNAL_EVIDENCE_MISSING'
        else:
            status='NOT_APPLICABLE'; reason='NO_RUNTIME_GENERATION_CONTROL_NOT_EXERCISED'
        refs=common+evidence.get(cid,[])
        results.append(_r(c,status,reason,refs))
    counts={s:sum(1 for r in results if r['status']==s) for s in CONTROL_STATUSES}
    blockers=[r['control_id'] for r in results if r['blocks_production'] and r['status']!='SATISFIED_REFERENCE']
    body={'schema_version':'1.0.0','assessment_id':stable_id('SECCTRL',bundle['handoff']['runtime_custody_run_id'],registry['registry_digest'],length=28),'runtime_custody_run_id':bundle['handoff']['runtime_custody_run_id'],'assessed_at':assessed_at,'control_registry_digest':registry['registry_digest'],'control_count':len(results),'results':results,'status_counts':counts,'production_blocker_count':len(blockers),'production_blockers':blockers,'all_production_controls_satisfied':not blockers,'reference_hardening_passed':counts['UNSATISFIED']==0}
    return with_digest(body,'assessment_digest')
