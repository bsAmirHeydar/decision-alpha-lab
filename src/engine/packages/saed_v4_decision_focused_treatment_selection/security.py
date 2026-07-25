FORBIDDEN_KEYS={'live_credentials','broker_password','broker_token','private_signing_key','protected_final_evidence','future_outcomes','order_sender'}
def scan_payload(value,path='$'):
    findings=[]
    if isinstance(value,dict):
        for k,v in value.items():
            if str(k).lower() in FORBIDDEN_KEYS:findings.append(f'{path}.{k}')
            findings.extend(scan_payload(v,f'{path}.{k}'))
    elif isinstance(value,list):
        for i,v in enumerate(value):findings.extend(scan_payload(v,f'{path}[{i}]'))
    return findings
def assert_secure_payload(value):
    f=scan_payload(value)
    if f:raise ValueError('forbidden security fields: '+','.join(f))
    return True
