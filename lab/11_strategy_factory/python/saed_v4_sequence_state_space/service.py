from __future__ import annotations
from .validation import validate_sequence_spec,validate_candidates,validate_reset_policy,validate_upstream
from .embeddings import FrozenEmbeddingTable
from .sequence import compile_points,compile_sequences,sequence_manifest,sequence_to_dict
from .reset import reset_policy_receipt
from .trainer import fit_candidate
from .metrics import evaluate_candidate,truncation_sensitivity
from .streaming import batch_streaming_parity,chunked_parity
from .snapshot import restart_parity,create_snapshot
from .probes import state_probe,stability_probe
from .ablation import architecture_ablation,future_suffix_audit
from .checkpoint import checkpoint_card
from .registry import build_registry
from .tournament import run_tournament
from .distillation import distill_state,distillation_report
from .controls import baseline_control
from .contamination import audit as contamination_audit
from .integrity import build_integrity_receipt
from .replay import replay_receipt
from .diff import semantic_diff
from .telemetry import telemetry
from .claims import claim_ledger
from .handoff import build_v4_13_handoff
from .security import sbom,incident_template
from .budget import compute_budget
from .provenance import provenance
from .canonical import content_hash

def build_reference_bundle(token_streams,encoder_checkpoint,tokenizer,checkpoint_registry,v4_11_handoff,config_raw,candidate_raw,reset_raw):
    spec=validate_sequence_spec(config_raw);candidates=validate_candidates(candidate_raw);reset=validate_reset_policy(reset_raw)
    upstream_validation=validate_upstream(v4_11_handoff,tokenizer,encoder_checkpoint,checkpoint_registry)
    table=FrozenEmbeddingTable(encoder_checkpoint,v4_11_handoff['encoder_checkpoint_hash']);binding=table.binding()
    points=compile_points(token_streams,table);sequences=compile_sequences(points,spec.max_context_steps);sequence_docs=[sequence_to_dict(s) for s in sequences]
    upstream_hashes={'v4_11_handoff_hash':v4_11_handoff['handoff_hash'],'tokenizer_hash':tokenizer['tokenizer_hash'],'encoder_checkpoint_hash':encoder_checkpoint['checkpoint_hash'],'checkpoint_registry_hash':checkpoint_registry['registry_hash']}
    manifest=sequence_manifest(sequences,upstream_hashes);reset_receipt=reset_policy_receipt(reset);contamination=contamination_audit(sequences)
    budget=compute_budget(len(candidates),128,spec.state_dim,spec.max_context_steps,60)
    model_map={};weights_map={};checkpoints=[];receipts=[];metrics=[];parities=[];chunks=[];restarts=[];probes=[];stabilities=[];truncations=[];suffix=[];cards=[]
    for cs in candidates:
        if not cs.enabled:continue
        model,w,ckpt,receipt=fit_candidate(cs,spec.input_dim,sequences,budget['training_pair_limit']);model_map[cs.candidate_id]=model;weights_map[cs.candidate_id]=w;checkpoints.append(ckpt);receipts.append(receipt)
        metric=evaluate_candidate(model,w,sequences);metrics.append(metric)
        seq=next(s for s in sequences if len(s.points)>=2)
        parity=batch_streaming_parity(model,seq);parities.append(parity);chunks.append(chunked_parity(model,seq,spec.chunk_size));restarts.append(restart_parity(model,seq,min(1,len(seq.points)-1)))
        probe=state_probe(model,sequences);probes.append(probe);stabilities.append(stability_probe(model,seq));truncations.append(truncation_sensitivity(model,w,sequences));suffix.append(future_suffix_audit(model,seq));cards.append(checkpoint_card(ckpt,metric,parity,probe,receipt))
    tournament=run_tournament(metrics,parities,probes);registry=build_registry(cards,tournament);control=baseline_control(tournament);ablation=architecture_ablation(metrics)
    champion_id=tournament['reference_champion_id'];champion=model_map[champion_id];distilled=distill_state(champion_id,champion.state_dim,max(2,champion.state_dim//2));distill_report=distillation_report(champion,sequences,distilled)
    snapshots=[]
    for seq in sequences:
        if seq.points:
            ys,state=champion.batch([p.vector for p in seq.points]);snapshots.append(create_snapshot(champion_id,state,seq.sequence_id,seq.points[-1].record_id))
    named={'upstream_validation':upstream_validation,'frozen_encoder_binding':binding,'sequence_manifest':manifest,'reset_policy':reset_receipt,'contamination_audit':contamination,'compute_budget':budget,'candidate_checkpoints':checkpoints,'training_receipts':receipts,'candidate_metrics':metrics,'streaming_parity':parities,'chunked_parity':chunks,'restart_parity':restarts,'state_probes':probes,'stability_probes':stabilities,'truncation_reports':truncations,'future_suffix_audits':suffix,'checkpoint_cards':cards,'tournament':tournament,'checkpoint_registry':registry,'baseline_control':control,'ablation_report':ablation,'distillation':distilled,'distillation_report':distill_report,'state_snapshots':snapshots,'sbom':sbom(),'incident_template':incident_template()}
    integrity=build_integrity_receipt(named);replay=replay_receipt(tournament,tournament);diff=semantic_diff(registry,registry);tele=telemetry(manifest,tournament,registry,parities);claims=claim_ledger(registry,tournament);prov=provenance(binding,content_hash({'config':config_raw,'candidates':candidate_raw,'reset':reset_raw}));handoff=build_v4_13_handoff(v4_11_handoff,registry,tournament,distilled,integrity,manifest)
    named.update({'integrity_receipt':integrity,'replay_receipt':replay,'semantic_diff':diff,'telemetry':tele,'claim_ledger':claims,'provenance':prov,'handoff':handoff})
    return named,sequence_docs
