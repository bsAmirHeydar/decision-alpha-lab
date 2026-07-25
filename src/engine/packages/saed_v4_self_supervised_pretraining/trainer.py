from __future__ import annotations
import time
from collections import defaultdict
from .encoder import ReferenceEmbeddingEncoder, checkpoint_payload
from .objectives import build_training_pairs
from .budget import assert_budget
from .canonical import content_hash, stable_id
from .errors import BudgetError, TrainingError

def train_reference_encoder(streams,tokenizer,config,corpus_manifest,split_manifest,objective_registry,compute_budget):
    assert_budget(config,compute_budget)
    start=time.time();encoder=ReferenceEmbeddingEncoder(tokenizer['vocabulary'],config.embedding_dim,config.seed)
    exposures=[];epoch_metrics=[];total_pairs=0;global_epoch=0
    for stage in config.curriculum:
        for local_epoch in range(stage.epochs):
            global_epoch+=1
            pairs=build_training_pairs(streams,tokenizer,config,stage.stage_id,local_epoch)
            losses=defaultdict(list)
            for ordinal,pair in enumerate(pairs):
                if total_pairs>=config.max_total_pairs: raise BudgetError('max_total_pairs exceeded')
                loss=encoder.train_pair(pair.anchor_token,pair.positive_token,pair.negative_tokens,config.learning_rate,pair.weight)
                losses[pair.objective_id].append(loss);total_pairs+=1
                exposures.append({"exposure_id":f'exp_{total_pairs:06d}',"stage_id":stage.stage_id,"epoch":global_epoch,"ordinal":ordinal,"record_id":pair.record_id,"objective_id":pair.objective_id,"objective_kind":pair.objective_kind,"anchor_hash":content_hash(pair.anchor_token),"positive_hash":content_hash(pair.positive_token),"negative_count":len(pair.negative_tokens),"weight":pair.weight})
            epoch_metrics.append({"stage_id":stage.stage_id,"epoch":global_epoch,"pair_count":len(pairs),"mean_loss_by_objective":{k:sum(v)/len(v) for k,v in sorted(losses.items())},"encoder_state_hash":encoder.state_hash()})
    elapsed=time.time()-start
    if elapsed>compute_budget['max_wall_seconds']: raise BudgetError('wall budget exceeded')
    exposure_payload={"phase":"SAED_V4_11","complete":True,"total_pairs":total_pairs,"entries":exposures,"max_total_pairs":config.max_total_pairs,"all_train_split":True}
    exposure_payload['ledger_id']=stable_id('exposureledger',exposure_payload);exposure_payload['ledger_hash']=content_hash(exposure_payload)
    receipt={"phase":"SAED_V4_11","status":"completed_reference_synthetic","deterministic":True,"corpus_manifest_hash":corpus_manifest['manifest_hash'],"split_manifest_hash":split_manifest['split_manifest_hash'],"tokenizer_hash":tokenizer['tokenizer_hash'],"objective_registry_hash":objective_registry['registry_hash'],"compute_budget_hash":compute_budget['budget_hash'],"config_hash":content_hash({"exact_version":config.exact_version,"seed":config.seed,"embedding_dim":config.embedding_dim,"learning_rate":config.learning_rate,"negative_samples":config.negative_samples,"max_total_pairs":config.max_total_pairs,"deterministic":config.deterministic,"objectives":[x.__dict__ for x in config.objectives],"curriculum":[{"stage_id":x.stage_id,"epochs":x.epochs,"objective_ids":list(x.objective_ids),"max_pairs_per_record":x.max_pairs_per_record} for x in config.curriculum]}),"exposure_ledger_hash":exposure_payload['ledger_hash'],"epoch_metrics":epoch_metrics,"total_pairs":total_pairs,"elapsed_seconds_accounting":0.0,"training_role":"synthetic_reference","outcome_supervision":False,"protected_evidence_used":False,"runtime_authority":False}
    receipt['receipt_id']=stable_id('trainingreceipt',receipt);receipt['receipt_hash']=content_hash(receipt)
    checkpoint=checkpoint_payload(encoder,{"corpus_manifest_hash":corpus_manifest['manifest_hash'],"split_manifest_hash":split_manifest['split_manifest_hash'],"tokenizer_hash":tokenizer['tokenizer_hash'],"objective_registry_hash":objective_registry['registry_hash'],"training_receipt_hash":receipt['receipt_hash'],"exposure_ledger_hash":exposure_payload['ledger_hash']})
    return encoder,exposure_payload,receipt,checkpoint
