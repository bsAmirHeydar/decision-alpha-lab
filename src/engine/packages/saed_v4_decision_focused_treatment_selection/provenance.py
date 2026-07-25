from __future__ import annotations
from .canonical import content_hash

def provenance_record(inputs,outputs,code_version='1.0.0'):
    row={'phase':'SAED_V4_20','code_version':code_version,'input_hashes':{k:content_hash(v) for k,v in sorted(inputs.items())},'output_hashes':{k:content_hash(v) for k,v in sorted(outputs.items())},'deterministic':True,'known_time_only':True,'protected_evidence_exposure':0}
    row['provenance_hash']=content_hash(row);return row
