from __future__ import annotations
from .errors import AuthorityError

FORBIDDEN_TRUE_KEYS = {
    'promotion_authority', 'production_authorization', 'runtime_executable',
    'risk_allocation_authority', 'execution_authority', 'order_submission',
    'activate_runtime', 'online_learning', 'mutate_policy', 'send_order'
}
FORBIDDEN_SECRET_MARKERS = ('-----BEGIN PRIVATE KEY-----', 'broker_password=', 'api_secret=')

def scan(value, path='$'):
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_TRUE_KEYS and item not in (False, None, 0, '', 'denied', 'forbidden', 'not_claimed'):
                raise AuthorityError(f'forbidden authority at {path}.{key}')
            scan(item, f'{path}.{key}')
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan(item, f'{path}[{index}]')
    elif isinstance(value, str):
        for marker in FORBIDDEN_SECRET_MARKERS:
            if marker.lower() in value.lower():
                raise AuthorityError(f'secret material at {path}')
    return True
