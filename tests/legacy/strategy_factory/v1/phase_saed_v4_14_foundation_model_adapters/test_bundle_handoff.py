def test_bundle_closed(bundle):
 required={'upstream_validation','intake_decisions','supply_chain_attestations','contamination_audit','token_sequence','compute_exposure_ledger','adapter_features','calibration_report','domain_shift_report','candidate_metrics','future_suffix_audits','fail_closed_audits','candidate_checkpoints','tournament','checkpoint_registry','integrity_receipt','replay_receipt','provenance','handoff','claim_ledger','sbom','incident_template','authority_boundary','bundle_hash'};assert set(bundle)==required
def test_tournament_baseline_preserved(bundle):assert bundle['tournament']['baseline_preserved'] and bundle['tournament']['production_authority'] is False
def test_registry_immutable_nonruntime(bundle):assert bundle['checkpoint_registry']['immutable'] and not bundle['checkpoint_registry']['runtime_authority']
def test_handoff_gates(bundle):assert bundle['handoff']['next_phase']=='SAED_V4_15' and all(bundle['handoff']['entry_gates'].values())
def test_handoff_authority_denials(bundle):
 a=bundle['handoff']['authority'];assert a['build_reference_multimodal_fusion'] and not any(a[k] for k in ['mutate_v4_14_evidence','load_unapproved_external_weights','invoke_remote_model','predict_outcomes','rank_treatments','select_treatment','allocate_risk','activate_runtime','send_order'])
def test_replay_deterministic(bundle):assert bundle['replay_receipt']['deterministic']
