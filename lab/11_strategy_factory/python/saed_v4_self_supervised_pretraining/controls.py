from __future__ import annotations
from .encoder import ReferenceEmbeddingEncoder, checkpoint_payload
from .evaluation import evaluate_representation
from .canonical import content_hash, stable_id

def build_control_comparison(trained_encoder,trained_checkpoint,streams,tokenizer,seed,dimension):
    random_encoder=ReferenceEmbeddingEncoder(tokenizer['vocabulary'],dimension,seed+100003)
    random_checkpoint=checkpoint_payload(random_encoder,{"control":"random_encoder","trained":False})
    frozen_encoder=ReferenceEmbeddingEncoder(tokenizer['vocabulary'],dimension,seed)
    frozen_checkpoint=checkpoint_payload(frozen_encoder,{"control":"frozen_initial_encoder","trained":False})
    trained=evaluate_representation(trained_encoder,streams,trained_checkpoint,'trained_reference')
    random=evaluate_representation(random_encoder,streams,random_checkpoint,'random_encoder')
    frozen=evaluate_representation(frozen_encoder,streams,frozen_checkpoint,'frozen_initial_encoder')
    payload={"phase":"SAED_V4_11","trained":trained,"random_control":random,"frozen_control":frozen,"from_scratch_control":{"status":"deferred_to_downstream_supervised_phase","reason":"V4-11 forbids outcome-specific supervised fitting"},"baseline_preserved":True,"automatic_superiority_claim":False}
    payload['comparison_id']=stable_id('controlcomparison',payload);payload['comparison_hash']=content_hash(payload);return payload
