from __future__ import annotations
from .validation import validate_records,validate_training_config
from .corpus import build_corpus_manifest,corpus_membership
from .splits import assign_splits
from .tokenization import build_token_streams,build_tokenizer_spec,stream_to_dict
from .masking import build_masking_plan
from .negatives import build_negative_plan
from .objectives import objective_registry
from .budget import build_compute_budget
from .trainer import train_reference_encoder
from .contamination import audit_contamination,assert_clean,membership_audit
from .evaluation import evaluate_representation
from .controls import build_control_comparison
from .checkpoint import checkpoint_card
from .registry import build_checkpoint_registry
from .integrity import build_integrity_receipt
from .replay import build_replay_receipt
from .diff import semantic_diff
from .telemetry import build_telemetry
from .claims import claim_ledger
from .handoff import build_v4_12_handoff

def build_reference_bundle(records_raw,upstream_manifest,handoff,config_raw,split_policy,canaries):
    records=validate_records(records_raw);config=validate_training_config(config_raw)
    corpus=build_corpus_manifest(records_raw,upstream_manifest,handoff);membership=corpus_membership(records_raw)
    splits=assign_splits(records,split_policy);streams=build_token_streams(records,splits);stream_docs=[stream_to_dict(s) for s in streams]
    tokenizer=build_tokenizer_spec(streams);masking=build_masking_plan(streams,config.seed);negatives=build_negative_plan(streams,tokenizer['vocabulary'],config.negative_samples,config.seed)
    objectives=objective_registry(config);budget=build_compute_budget(config.max_total_pairs,sum(x.epochs for x in config.curriculum),config.embedding_dim,30.0)
    contamination=audit_contamination(records_raw,splits,stream_docs,canaries);assert_clean(contamination)
    encoder,exposure,training_receipt,checkpoint=train_reference_encoder(streams,tokenizer,config,corpus,splits,objectives,budget)
    dossier=evaluate_representation(encoder,streams,checkpoint);member_audit=membership_audit(checkpoint,canaries)
    controls=build_control_comparison(encoder,checkpoint,streams,tokenizer,config.seed,config.embedding_dim)
    registry=build_checkpoint_registry(checkpoint,dossier,contamination,member_audit,controls)
    card=checkpoint_card(checkpoint,training_receipt,dossier)
    named={"corpus_manifest":corpus,"membership":membership,"split_manifest":splits,"tokenizer":tokenizer,"masking":masking,"negatives":negatives,"objectives":objectives,"budget":budget,"exposure":exposure,"training_receipt":training_receipt,"checkpoint":checkpoint,"dossier":dossier,"controls":controls,"contamination":contamination,"membership_audit":member_audit,"registry":registry,"checkpoint_card":card}
    integrity=build_integrity_receipt(named)
    replay=build_replay_receipt(training_receipt,training_receipt)
    diff=semantic_diff(checkpoint,checkpoint)
    telemetry=build_telemetry(corpus,splits,tokenizer,training_receipt,dossier,registry,contamination)
    claims=claim_ledger(registry['admitted_count']==1)
    handoff12=build_v4_12_handoff(registry,checkpoint,tokenizer,corpus,splits,training_receipt,dossier,integrity)
    named.update({"integrity":integrity,"replay":replay,"semantic_diff":diff,"telemetry":telemetry,"claims":claims,"handoff":handoff12})
    return named,stream_docs
