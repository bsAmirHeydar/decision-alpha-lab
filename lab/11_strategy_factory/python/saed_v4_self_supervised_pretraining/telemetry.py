from __future__ import annotations
from .canonical import content_hash, stable_id

def build_telemetry(corpus,split_manifest,tokenizer,training_receipt,dossier,registry,contamination):
    payload={"phase":"SAED_V4_11","implementation_status":"implemented_reference_synthetic","corpus_record_count":corpus['record_count'],"split_counts":split_manifest['counts'],"vocabulary_size":tokenizer['vocabulary_size'],"training_pair_count":training_receipt['total_pairs'],"training_status":training_receipt['status'],"representation_collapsed":dossier['collapse']['collapsed'],"reference_checkpoint_admitted":registry['admitted_count']==1,"contamination_passed":contamination['passed'],"external_evidence":{"real_corpus_training":"not_claimed","distributed_training":"not_claimed","gpu_reproduction":"not_claimed","metaeditor_compile":"pending_local_windows","prospective_paper":"not_claimed","shadow":"not_claimed","live":"not_claimed"},"authority":{"runtime":False,"selection":False,"execution":False}}
    payload['telemetry_id']=stable_id('v411telemetry',payload);payload['telemetry_hash']=content_hash(payload);return payload
