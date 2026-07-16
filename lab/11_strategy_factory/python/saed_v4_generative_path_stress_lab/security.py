from __future__ import annotations
from .errors import AuthorityError
FORBIDDEN_KEYS={'api_key','secret','password','token','live_credential','broker_credential','protected_final_evidence','hidden_evaluation_label','live_order','order_ticket'}
def scan(value,path='$'):
    if isinstance(value,dict):
        for k,v in value.items():
            if str(k).lower() in FORBIDDEN_KEYS: raise AuthorityError(f'forbidden key at {path}.{k}')
            scan(v,f'{path}.{k}')
    elif isinstance(value,list):
        for i,v in enumerate(value):scan(v,f'{path}[{i}]')
    return True
