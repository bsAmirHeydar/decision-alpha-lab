from __future__ import annotations
from .canonical import content_hash, stable_id
from .encoder import encoder_from_checkpoint
from .errors import CheckpointError

def validate_checkpoint(checkpoint:dict)->None:
    encoder_from_checkpoint(checkpoint)
    if checkpoint.get('runtime_authority') is not False or checkpoint.get('selection_authority') is not False or checkpoint.get('execution_authority') is not False: raise CheckpointError('checkpoint carries forbidden authority')
    if checkpoint.get('synthetic_reference_only') is not True: raise CheckpointError('reference checkpoint watermark missing')
    if checkpoint.get('checkpoint_format')!='json_embedding_table_v1': raise CheckpointError('unsupported checkpoint format')

def checkpoint_card(checkpoint:dict,training_receipt:dict,dossier:dict)->dict:
    validate_checkpoint(checkpoint)
    payload={"phase":"SAED_V4_11","checkpoint_id":checkpoint['checkpoint_id'],"checkpoint_hash":checkpoint['checkpoint_hash'],"model_family":checkpoint['model_family'],"dimension":checkpoint['dimension'],"vocabulary_size":len(checkpoint['vocabulary']),"training_receipt_hash":training_receipt['receipt_hash'],"representation_dossier_hash":dossier['dossier_hash'],"intended_use":"offline representation research and V4-12 sequence-model input only","prohibited_uses":["treatment ranking","treatment selection","risk allocation","runtime activation","order placement"],"evidence_scope":"synthetic_reference","known_limitations":dossier['limitations']}
    payload['card_id']=stable_id('checkpointcard',payload);payload['card_hash']=content_hash(payload);return payload
