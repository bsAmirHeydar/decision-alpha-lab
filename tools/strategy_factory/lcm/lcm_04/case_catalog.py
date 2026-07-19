from __future__ import annotations
from .canonical import digest_object
from .registries import CASE_TYPES

DESCRIPTIONS={
 'POSITIVE':'Legacy conditions produce the expected positive event path.',
 'NEGATIVE':'Inputs remain ineligible and no positive event is emitted.',
 'NO_TRADE':'The system explicitly abstains with a stable reason.',
 'INVALIDATION':'An active reference or setup is invalidated at the declared boundary.',
 'EXPIRY':'A pending state expires without hidden carry-over.',
 'RESTART':'State after process/chart restart follows the declared persistence policy.',
 'HISTORY_EXPANSION':'Additional historical bars do not rewrite known-time decisions.',
 'MISSING_BAR':'Incomplete data produces explicit failure or abstention.',
 'DST_TRANSITION':'Timezone and daylight-saving transition semantics remain stable.',
 'SESSION_BOUNDARY':'Session open/close boundaries are deterministic.',
 'TIMEFRAME_CHANGE':'Chart or requested timeframe change follows the declared policy.',
 'SYMBOL_CHANGE':'Symbol change does not leak stale cross-symbol state.',
 'MULTI_INSTANCE':'Multiple instances do not collide in state or object names.',
 'DUPLICATE_TICK':'Repeated delivery of the same tick/event is idempotent.',
 'CURRENT_BAR_INTRABAR':'Intrabar behavior is captured rather than inferred from drawings.',
 'CLOSED_BAR_CONFIRMATION':'Closed-bar authority is captured explicitly.',
 'DRAWING_LIFECYCLE':'Anchors, object IDs, updates and deletion ownership are captured.',
 'DRY_EXECUTION_REQUEST':'Normalized request intent is captured with broker submission disabled.'}

def build():
    rows=[]
    for idx,case_type in enumerate(CASE_TYPES,1):
        row={'case_type':case_type,'ordinal':idx,'description':DESCRIPTIONS[case_type],
             'required_input_classes':['TIME','STATE','DATA_AVAILABILITY'],
             'broker_submission_allowed':False,'semantic_correction_allowed':False,
             'case_contract_digest':None}
        row['case_contract_digest']=digest_object(row,'case_contract_digest');rows.append(row)
    obj={'schema_version':'1.0.0','phase_id':'LCM-04','catalog_id':'LCM04_GOLDEN_CASE_CATALOG_V1','closed':True,
         'case_count':len(rows),'cases':rows,'dynamic_case_type_allowed':False,'catalog_digest':None}
    obj['catalog_digest']=digest_object(obj,'catalog_digest');return obj

def required_cases(profile):
    caps=profile['capabilities'];out={'POSITIVE','NEGATIVE','NO_TRADE','RESTART','DUPLICATE_TICK'}
    if caps['timeframe_api'] or caps['current_bar'] or caps['closed_bar']:
        out|={'HISTORY_EXPANSION','MISSING_BAR','TIMEFRAME_CHANGE','CURRENT_BAR_INTRABAR','CLOSED_BAR_CONFIRMATION'}
    if caps['session_api'] or caps['wall_clock']: out|={'DST_TRANSITION','SESSION_BOUNDARY'}
    if caps['drawing_api']: out|={'DRAWING_LIFECYCLE','MULTI_INSTANCE','SYMBOL_CHANGE'}
    if caps['order_api']: out|={'DRY_EXECUTION_REQUEST','INVALIDATION','EXPIRY'}
    if caps['global_state'] or caps['timer_api']: out|={'RESTART','MULTI_INSTANCE'}
    return sorted(out)
