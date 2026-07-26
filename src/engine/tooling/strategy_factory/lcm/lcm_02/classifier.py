from __future__ import annotations
import json,re
from .canonical import content_id,digest_object
from .ownership import owner_binding
from .registries import PROTECTED_FAMILIES,SECURITY_CAPABILITIES

DOMAIN_FAMILIES={'M_SERIES_CONTEXTS','EXP0015_INTERMARKET_TIME','EXP0016_INTERMARKET_EXECUTION','EXP0017_CYCLE_GROUP','EXP0018_DAYE_TRADER','EXP0019_FAERIE_PROTOCOL','FLAG_COUNTING_NDS_HOOK_ZONE','ICT_STRUCTURAL_NODES','ASTRO_RESEARCH_EXECUTION','EXECUTION_E_SERIES','RESEARCH_EXPERIMENTS'}
RELEASE_FAMILIES={'PATCH_AND_RELEASE_ARCHIVE','ROOT_RELEASE_AND_INSTALLATION_HISTORY'}

def _contains(path,*tokens):
    p=path.lower(); return any(t in p for t in tokens)
def role_for(row, caps: set[str]):
    path=row['path']; p=path.lower(); fam=row['family_candidate']; lang=row['language']; ext=row['extension']; survey=row.get('semantic_role_candidate','UNKNOWN_ROLE')
    evidence=[]
    if '/tests' in p or p.startswith('tests/') or '/test_' in p or p.endswith('_test.py'):
        return ('TEST_CODE',9000,['PATH_TEST_CONVENTION'])
    if '/fixtures/' in p or p.startswith('data/') and _contains(p,'fixture','sample','reference'):
        return ('TEST_FIXTURE',8500,['PATH_FIXTURE_CONVENTION'])
    if fam in RELEASE_FAMILIES or _contains(p,'patch_manifest','file_hashes','file_index','qa_report','commit_message','expand_remove','install_'):
        return ('RELEASE_METADATA',9500,['RELEASE_FILENAME_OR_FAMILY'])
    if ext in {'.zip','.blob'} or fam in {'OTHER_PAPERS','OTHER_LICENSES'}:
        return ('ARCHIVE',8000,['BINARY_OR_ARCHIVE_FAMILY'])
    if p.startswith('.github/') or path in {'AGENTS.md','CONTRIBUTING.md','CODE_OF_CONDUCT.md','.editorconfig','.gitattributes','.gitignore'}:
        return ('GOVERNANCE_CONTROL',9500,['REPOSITORY_GOVERNANCE_PATH'])
    if _contains(p,'13_atomic_concepts','12_phase_deliveries','obsidian_deep','source_cards','generated/'):
        return ('GENERATED_PROJECTION',9000,['GENERATED_DOCUMENTATION_NAMESPACE'])
    if p.startswith('registry/') or _contains(p,'/schemas/','/policies/') or lang in {'YAML','JSON','TOML','INI'} and _contains(p,'contract','registry','schema','policy','config'):
        return ('CONFIGURATION_CONTRACT',8500,['MACHINE_CONTRACT_PATH'])
    if fam in PROTECTED_FAMILIES or p.startswith('src/engine/legacy/acl_os_reference/') or p.startswith('src/engine/tooling/strategy_factory/lcm/'):
        return ('PLATFORM_KERNEL',9500,['PROTECTED_PLATFORM_FAMILY_OR_PATH'])
    if lang=='MARKDOWN' or ext in {'.pdf','.canvas'}:
        if _contains(p,'source','doctrine','manifesto','principles','thesis','research_memory'):
            return ('SOURCE_EVIDENCE',7000,['DOCUMENT_SOURCE_OR_DOCTRINE_TOKEN'])
        return ('DOCUMENTATION',7000,['DOCUMENT_MEDIA'])
    if 'ORDER_API' in caps or fam in {'EXECUTION_E_SERIES','EXP0016_INTERMARKET_EXECUTION'}:
        return ('EXECUTION_ADAPTER',9000,['ORDER_CAPABILITY_OR_EXECUTION_FAMILY'])
    if _contains(p,'diagnostic','anatomy','debug','trace'):
        return ('DIAGNOSTIC',8500,['DIAGNOSTIC_PATH_TOKEN'])
    if _contains(p,'visual','draw','drawing','renderer','panel','indicator') and ('DRAWING_API' in caps or lang in {'MQL5_COMPILE_UNIT','MQL5_HEADER'}):
        return ('VISUALIZER',8000,['VISUAL_PATH_AND_DRAWING_EVIDENCE'])
    if _contains(p,'treatment','entry','exit','stop','target','risk','position_management'):
        return ('TREATMENT',7500,['TREATMENT_PATH_TOKEN'])
    if _contains(p,'setup','signal','trigger','confirmation','eligibility'):
        return ('SETUP',7500,['SETUP_PATH_TOKEN'])
    if _contains(p,'context','state','session','divergence','hunt','cycle','zone','flag','nds','hook') and fam in DOMAIN_FAMILIES:
        return ('CONTEXT',7000,['DOMAIN_FAMILY_AND_CONTEXT_TOKEN'])
    if _contains(p,'adapter','bridge','compat','platform'):
        return ('PLATFORM_ADAPTER',7000,['ADAPTER_PATH_TOKEN'])
    if _contains(p,'shared','common','kernel','engine','utility','utils','primitive') and lang in {'PYTHON','MQL5_HEADER'}:
        return ('SHARED_PRIMITIVE',7000,['SHARED_PRIMITIVE_PATH_TOKEN'])
    if fam in DOMAIN_FAMILIES:
        if _contains(p,'research','experiment','backtest','analysis'):
            return ('RESEARCH',7000,['RESEARCH_PATH_TOKEN'])
        if lang in {'MQL5_COMPILE_UNIT','MQL5_HEADER','PYTHON'}:
            return ('UNKNOWN_ROLE',0,['DOMAIN_CODE_ROLE_AMBIGUOUS'])
    if survey!='UNKNOWN_ROLE':
        mapping={'EXECUTABLE_OR_SERVICE':'PLATFORM_ADAPTER','TEST_OR_FIXTURE':'TEST_FIXTURE','DOCUMENTATION_OR_KNOWLEDGE_ARTIFACT':'DOCUMENTATION','CONFIGURATION_OR_DATA_CONTRACT':'CONFIGURATION_CONTRACT','RELEASE_OR_INSTALLATION_METADATA':'RELEASE_METADATA'}
        if survey in mapping: return (mapping[survey],6000,['LCM01_SEMANTIC_ROLE_CANDIDATE'])
    return ('UNKNOWN_ROLE',0,['INSUFFICIENT_STATIC_ROLE_EVIDENCE'])

def activity_for(row, role: str, entry: set[str], inbound: int):
    path=row['path']; fam=row['family_candidate']; p=path.lower()
    if role in {'TEST_CODE','TEST_FIXTURE'}: return ('TEST_ONLY',9000,['TEST_ROLE'])
    if role=='GENERATED_PROJECTION': return ('GENERATED',9000,['GENERATED_ROLE'])
    if role=='ARCHIVE': return ('ARCHIVED',9000,['ARCHIVE_ROLE'])
    if role=='RELEASE_METADATA': return ('RELEASE_HISTORY',9000,['RELEASE_ROLE'])
    if role=='DOCUMENTATION' or role=='SOURCE_EVIDENCE': return ('DOCUMENTATION_ONLY',7500,['DOCUMENT_ROLE'])
    if role in {'CONFIGURATION_CONTRACT','GOVERNANCE_CONTROL'}: return ('CONFIGURATION',8000,['CONFIGURATION_ROLE'])
    if fam in PROTECTED_FAMILIES and row['language'] in {'PYTHON','MQL5_COMPILE_UNIT','MQL5_HEADER'}: return ('ACTIVE_PLATFORM',8500,['PROTECTED_PLATFORM_CODE'])
    if path in entry:
        if row['language']=='MQL5_COMPILE_UNIT': return ('ACTIVE_RUNTIME_CANDIDATE',8500,['MQL5_COMPILE_UNIT_ENTRY'])
        return ('ACTIVE_RESEARCH',8000,['PYTHON_ENTRY_POINT'])
    if inbound>0 and row['language'] in {'PYTHON','MQL5_HEADER'}:
        if fam in DOMAIN_FAMILIES: return ('ACTIVE_RESEARCH',6500,['RESOLVED_INBOUND_DEPENDENCY'])
        return ('ACTIVE_PLATFORM',6500,['RESOLVED_INBOUND_DEPENDENCY'])
    if fam in DOMAIN_FAMILIES and row['language'] in {'PYTHON','MQL5_COMPILE_UNIT','MQL5_HEADER'}:
        return ('UNKNOWN_ACTIVITY',0,['STATIC_REACHABILITY_NOT_PROVEN'])
    return ('UNKNOWN_ACTIVITY',0,['ACTIVITY_NOT_PROVEN'])

def surfaces_for(caps: set[str], path: str):
    m={'ORDER_API':'ORDER_REQUEST','FILE_IO':'FILE_PERSISTENCE','FILE_MUTATION':'FILE_PERSISTENCE','NETWORK_API':'NETWORK_EGRESS','DYNAMIC_IMPORT':'DYNAMIC_CODE','DYNAMIC_EVAL':'DYNAMIC_CODE','DYNAMIC_COMPILE':'DYNAMIC_CODE','SUBPROCESS':'DYNAMIC_CODE','GLOBAL_VARIABLE_API':'GLOBAL_STATE','PERSISTENT_STATE':'GLOBAL_STATE','DRAWING_API':'CHART_STATE','CHART_CALLBACK':'CHART_STATE','TIMEFRAME_ACCESS':'TIME_SEMANTICS','SESSION_OR_DST_TERMS':'TIME_SEMANTICS','MULTI_SYMBOL_ACCESS':'BROKER_STATE','SECRET_GENERATION_INDICATOR':'EXTERNAL_MODEL'}
    s={m[c] for c in caps if c in m}
    if 'ORDER_REQUEST' in s: s.update({'BROKER_STATE','CAPITAL'})
    return sorted(s)

def disposition_for(row, role: str, activity: str, caps: set[str], duplicate: bool, protected: bool):
    if caps & SECURITY_CAPABILITIES: return ('SECURITY_RESTRICTED',['SECURITY_CAPABILITY_PRESENT'])
    # Generated projections and release/archive history remain non-canonical even when
    # they live under a protected platform namespace. Protection prevents destructive
    # migration; it does not elevate derived material to canonical doctrine.
    if role in {'GENERATED_PROJECTION','RELEASE_METADATA','ARCHIVE'}: return ('ARCHIVE_REFERENCE_ONLY',['NON_CANONICAL_HISTORY_OR_PROJECTION'])
    if protected: return ('KEEP_CANONICAL',['PROTECTED_PLATFORM_ASSET'])
    if duplicate: return ('MERGE_AFTER_EQUIVALENCE_PROOF',['EXACT_BYTE_DUPLICATE_REQUIRES_EQUIVALENCE_REVIEW'])
    if role=='UNKNOWN_ROLE' or activity=='UNKNOWN_ACTIVITY': return ('QUARANTINE_UNCERTAIN',['ROLE_OR_ACTIVITY_UNKNOWN'])
    if role=='SHARED_PRIMITIVE': return ('EXTRACT_SHARED_LOGIC',['SHARED_PRIMITIVE_CANDIDATE'])
    if role in {'CONTEXT','SETUP','TREATMENT','VISUALIZER','PLATFORM_ADAPTER','EXECUTION_ADAPTER','RESEARCH','DIAGNOSTIC'}:
        complex_caps={'PERSISTENT_STATE','GLOBAL_VARIABLE_API','TIMER_API','TIMEFRAME_ACCESS','SESSION_OR_DST_TERMS','MULTI_SYMBOL_ACCESS','FILE_IO','DRAWING_API'}
        if caps & complex_caps: return ('REWRITE_WITH_PARITY',['BEHAVIORALLY_COMPLEX_LEGACY_LOGIC'])
        return ('WRAP_LEGACY',['LEGACY_DOMAIN_OR_ADAPTER_ROLE'])
    if role in {'DOCUMENTATION','SOURCE_EVIDENCE','CONFIGURATION_CONTRACT','GOVERNANCE_CONTROL','TEST_CODE','TEST_FIXTURE'}:
        return ('MOVE_WITHOUT_SEMANTIC_CHANGE',['STRUCTURAL_RELOCATION_CANDIDATE'])
    return ('QUARANTINE_UNCERTAIN',['NO_SAFE_PRIMARY_DISPOSITION'])

def classify(row, caps: set[str], entry: set[str], inbound: int, duplicate: bool):
    role,rc,rev=role_for(row,caps)
    activity,ac,aev=activity_for(row,role,entry,inbound)
    protected=row['family_candidate'] in PROTECTED_FAMILIES or row['path'].startswith(('src/engine/legacy/acl_os_reference/','src/engine/tooling/strategy_factory/lcm/','registry/history/lcm/'))
    surfaces=surfaces_for(caps,row['path']); security=bool(caps & SECURITY_CAPABILITIES)
    disp,dev=disposition_for(row,role,activity,caps,duplicate,protected)
    owner=owner_binding(row['family_candidate'],role,security)
    blockers=list(owner['ownership_blockers'])
    if role=='UNKNOWN_ROLE': blockers.append('SEMANTIC_ROLE_UNRESOLVED')
    if activity=='UNKNOWN_ACTIVITY': blockers.append('ACTIVITY_UNRESOLVED')
    if security: blockers.append('SECURITY_REVIEW_REQUIRED')
    if duplicate: blockers.append('DUPLICATE_EQUIVALENCE_REVIEW_REQUIRED')
    if role=='GENERATED_PROJECTION': blockers.append('GENERATED_PROJECTION_NON_CANONICAL')
    canonical='NON_CANONICAL_GENERATED' if role=='GENERATED_PROJECTION' else ('PROTECTED_PLATFORM_CANONICAL' if protected else 'CANONICAL_SELECTION_NOT_PERFORMED')
    rec={'schema_version':'1.0.0','classification_id':content_id('ARTCLS',[row['path'],row['sha256']]),'artifact_path':row['path'],'artifact_sha256':row['sha256'],'source_layer_id':row['source_layer_id'],'family_candidate':row['family_candidate'],'family_confidence_bps':int(row['family_confidence_bps']),'artifact_role':role,'role_confidence_bps':rc,'role_evidence_codes':rev,'activity_status':activity,'activity_confidence_bps':ac,'activity_evidence_codes':aev,'primary_disposition':disp,'disposition_evidence_codes':dev,'protected_platform_asset':protected,'canonical_selection_status':canonical,'generated_projection_canonical_authority':False,'duplicate_member':duplicate,'capability_kinds':sorted(caps),'authority_surfaces':surfaces,'security_sensitive':security,'authority_is_risk_indicator_only':True,'live_authority_inferred':False,'source_move_authorized':False,'source_delete_authorized':False,'semantic_refactor_authorized':False,'merge_authorized':False,'cutover_authorized':False,'runtime_authorized':False,'live_order_authorized':False,'capital_authorized':False,**owner,'blocking_reasons':sorted(set(blockers)),'classification_is_domain_semantic_approval':False}
    rec['classification_digest']=digest_object(rec,'classification_digest'); return rec
