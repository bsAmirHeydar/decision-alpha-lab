from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash, stable_id
from .validation import validate_upstream_manifest,validate_v4_10_handoff,validate_records,validate_training_config
from .errors import SelfSupervisedPretrainingError

def run_conformance(vectors:dict)->dict:
    results=[]
    for case in vectors['cases']:
        passed=False;error_type=None
        try:
            kind=case['kind'];payload=deepcopy(case['payload'])
            if kind=='upstream_manifest': validate_upstream_manifest(payload)
            elif kind=='handoff': validate_v4_10_handoff(payload,case['companion'])
            elif kind=='records': validate_records(payload)
            elif kind=='training_config': validate_training_config(payload)
            else: raise ValueError('unknown conformance kind')
            passed=True
        except Exception as e:
            error_type=type(e).__name__
        expected=case['expected_valid']
        results.append({"case_id":case['case_id'],"expected_valid":expected,"observed_valid":passed,"matched":passed==expected,"error_type":error_type})
    payload={"phase":"SAED_V4_11","results":results,"passed":all(x['matched'] for x in results),"case_count":len(results)}
    payload['result_id']=stable_id('conformance',payload);payload['result_hash']=content_hash(payload);return payload
