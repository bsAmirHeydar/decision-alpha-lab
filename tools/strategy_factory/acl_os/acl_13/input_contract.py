from __future__ import annotations
from datetime import datetime
from .canonical import verify_embedded_digest,with_digest
from .errors import ContractError
def _dt(v:str)->datetime: return datetime.fromisoformat(v.replace('Z','+00:00'))
def validate_request(req:dict)->dict:
    if not verify_embedded_digest(req,'assessment_request_digest'): raise ContractError('ACL13_REQUEST_DIGEST_INVALID')
    if req.get('schema_version')!='1.0.0': raise ContractError('ACL13_REQUEST_VERSION_INVALID')
    required=['assessment_request_id','context_id','context_version','owner_roles','doctrine_summary','assessment_cut_at','known_time_contract','observations','declared_setup_families']
    if any(k not in req for k in required): raise ContractError('ACL13_REQUEST_FIELD_MISSING')
    if not req['owner_roles'] or not req['doctrine_summary'].strip(): raise ContractError('ACL13_OWNER_OR_DOCTRINE_MISSING')
    if req['known_time_contract'].get('future_data_allowed') is not False: raise ContractError('ACL13_FUTURE_DATA_AUTHORITY_DENIED')
    cut=_dt(req['assessment_cut_at']); ids=set()
    for row in req['observations']:
        oid=row.get('observation_id')
        if not oid or oid in ids: raise ContractError('ACL13_OBSERVATION_ID_INVALID')
        ids.add(oid)
        event=_dt(row['event_time']); available=_dt(row['available_at']); label=_dt(row['label_available_at'])
        if event>available or available>cut or label>cut: raise ContractError('ACL13_KNOWN_TIME_VIOLATION')
        if row.get('direction') not in {'LONG','SHORT','NONE'}: raise ContractError('ACL13_DIRECTION_INVALID')
    famids=[x.get('family_id') for x in req['declared_setup_families']]
    if len(famids)!=len(set(famids)) or not famids: raise ContractError('ACL13_SETUP_FAMILY_INVALID')
    body={'schema_version':'1.0.0','assessment_request_id':req['assessment_request_id'],'context_id':req['context_id'],'context_version':req['context_version'],'observation_count':len(req['observations']),'declared_setup_family_count':len(req['declared_setup_families']),'assessment_cut_at':req['assessment_cut_at'],'known_time_safe':True,'source_request_digest':req['assessment_request_digest']}
    return with_digest(body,'input_validation_digest')
