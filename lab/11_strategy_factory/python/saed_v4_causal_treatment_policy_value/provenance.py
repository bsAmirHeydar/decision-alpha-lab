from .canonical import content_hash

def build_provenance(inputs,outputs):
    out={'phase':'SAED_V4_18','input_hashes':inputs,'output_hashes':outputs,'known_time_only':True,'synthetic_only':True,'protected_evidence_exposures':0,'hidden_evaluation_queries':0};out['provenance_hash']=content_hash(out);return out
