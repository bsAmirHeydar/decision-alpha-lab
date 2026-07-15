from __future__ import annotations
from .canonical import content_hash, stable_id
from .validation import validate_corpus_manifest

def build_pretraining_corpus_manifest(view_package:dict,hypergraph:dict,lattice:dict)->dict:
    included=[
      {"artifact_class":"multimodal_view_package","artifact_id":view_package['package_id'],"artifact_hash":view_package['package_hash'],"role":"self_supervised_input","known_as_of":view_package['known_as_of']},
      {"artifact_class":"semantic_temporal_hypergraph","artifact_id":hypergraph['graph_id'],"artifact_hash":hypergraph['graph_hash'],"role":"self_supervised_structure","known_as_of":hypergraph['known_as_of']},
      {"artifact_class":"action_lattice_descriptors","artifact_id":lattice['lattice_id'],"artifact_hash":lattice['lattice_hash'],"role":"descriptor_vocabulary_only","known_as_of":None},
    ]
    payload={"phase":"SAED_V4_10","target_phase":"SAED_V4_11","included_artifacts":included,"prohibited_input_artifact_classes":["outcome_cube","execution_twin","benchmark_result","protected_final","prospective","shadow","live"],"self_supervised_only":True,"label_semantics":"none","future_suffix_allowed":False,"masked_objective_boundary":["feature_value_masking","view_presence_prediction","temporal_order_consistency","graph_relation_reconstruction"],"forbidden_objectives":["outcome_prediction","treatment_ranking","policy_value","live_fill_prediction"],"split_policy":"identity_and_time_partition_required_before_training","training_authority":False,"selection_authority":False,"execution_authority":False}
    validate_corpus_manifest(payload)
    payload['manifest_id']=stable_id('pretraincorpus',payload);payload['manifest_hash']=content_hash(payload)
    return payload
