from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from typing import Iterable
import math, re
from .enums import *
from .hashing import stable_id, sha256_lines, cfloat, cbool

SCHEMA_PREFIX = "alpha_lab.strategy_factory"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

def _required(*values: str) -> None:
    if any(not value for value in values):
        raise ValueError("missing required identity or lineage")

def _sha(value: str, label: str) -> None:
    if not _SHA256.fullmatch(value):
        raise ValueError(f"{label} must be lowercase sha256")

@dataclass(frozen=True, slots=True)
class ArtifactDigest:
    logical_name: str
    relative_path: str
    role: ArtifactRole
    media_type: str
    byte_size: int
    sha256: str
    schema_id: str = ""
    required: bool = True
    digest_id: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/artifact_digest@1.0.0", self.logical_name,
            self.relative_path, int(self.role), self.media_type, self.byte_size, self.sha256,
            self.schema_id, cbool(self.required)]))

    def with_id(self) -> "ArtifactDigest":
        return replace(self, digest_id=stable_id("adig", self.canonical()))

    def validate(self) -> None:
        _required(self.logical_name, self.relative_path, self.media_type)
        if self.relative_path.startswith(("/", "\\")) or ".." in self.relative_path.replace("\\", "/").split("/"):
            raise ValueError("artifact path must be repository-relative and traversal-free")
        if self.byte_size < 0:
            raise ValueError("artifact byte size cannot be negative")
        _sha(self.sha256, "artifact digest")
        expected = stable_id("adig", self.canonical())
        if self.digest_id and self.digest_id != expected:
            raise ValueError("artifact digest identity mismatch")

@dataclass(frozen=True, slots=True)
class ArtifactInventory:
    inventory_id: str
    inventory_version: str
    digests: tuple[ArtifactDigest, ...]
    generated_at_utc_msc: int
    inventory_hash: str = ""

    def canonical_root(self) -> str:
        ordered=sorted((d.digest_id or d.with_id().digest_id) for d in self.digests)
        return sha256_lines(ordered)

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/artifact_inventory@1.0.0",
            self.inventory_id, self.inventory_version, self.canonical_root(),
            len(self.digests), self.generated_at_utc_msc]))

    def with_hash(self) -> "ArtifactInventory":
        digests=tuple(d if d.digest_id else d.with_id() for d in self.digests)
        candidate=replace(self,digests=digests,inventory_hash="")
        return replace(candidate,inventory_hash=sha256_lines([candidate.canonical()]))

    def validate(self) -> None:
        _required(self.inventory_id,self.inventory_version)
        names=set();paths=set()
        for digest in self.digests:
            digest.validate()
            if digest.logical_name in names:raise ValueError("duplicate artifact logical name")
            if digest.relative_path in paths:raise ValueError("duplicate artifact relative path")
            names.add(digest.logical_name);paths.add(digest.relative_path)
        if self.generated_at_utc_msc<0:raise ValueError("invalid inventory timestamp")
        expected=self.with_hash().inventory_hash
        if self.inventory_hash and self.inventory_hash!=expected:
            raise ValueError("artifact inventory hash mismatch")

@dataclass(frozen=True, slots=True)
class AuthenticityAttestation:
    kind: AttestationKind
    subject_inventory_hash: str
    signer_id: str
    algorithm: str
    key_id: str
    signature_reference: str
    verifier_id: str
    verified: bool
    signed_at_utc_msc: int
    attestation_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/authenticity_attestation@1.0.0",
            int(self.kind), self.subject_inventory_hash, self.signer_id, self.algorithm, self.key_id,
            self.signature_reference, self.verifier_id, cbool(self.verified), self.signed_at_utc_msc]))

    def with_hash(self) -> "AuthenticityAttestation":
        return replace(self, attestation_hash=stable_id("attn", self.canonical()))

    def validate(self) -> None:
        _required(self.subject_inventory_hash)
        _sha(self.subject_inventory_hash, "subject inventory hash")
        if self.kind == AttestationKind.NONE:
            if self.verified or any((self.signer_id, self.algorithm, self.key_id, self.signature_reference, self.verifier_id)):
                raise ValueError("unsigned attestation cannot claim signature verification")
        else:
            _required(self.signer_id, self.algorithm, self.key_id, self.signature_reference, self.verifier_id)
            if not self.verified:
                raise ValueError("signature-bearing attestation must be externally verified")
        if self.signed_at_utc_msc < 0:
            raise ValueError("invalid attestation timestamp")
        expected = stable_id("attn", self.canonical())
        if self.attestation_hash and self.attestation_hash != expected:
            raise ValueError("attestation hash mismatch")

@dataclass(frozen=True, slots=True)
class RegistryScope:
    strategy_id: str
    anatomy_plugin_id: str
    anatomy_plugin_version: str
    symbol_universe_id: str
    timeframe_profile_id: str
    deployment_profile_id: str
    feature_schema_hash: str
    label_contract_hash: str
    scope_id: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/registry_scope@1.0.0", self.strategy_id,
            self.anatomy_plugin_id, self.anatomy_plugin_version, self.symbol_universe_id,
            self.timeframe_profile_id, self.deployment_profile_id, self.feature_schema_hash,
            self.label_contract_hash]))

    def with_id(self) -> "RegistryScope":
        return replace(self, scope_id=stable_id("scope", self.canonical()))

    def validate(self) -> None:
        _required(self.strategy_id, self.anatomy_plugin_id, self.anatomy_plugin_version,
                  self.symbol_universe_id, self.timeframe_profile_id, self.deployment_profile_id,
                  self.feature_schema_hash, self.label_contract_hash)
        expected = stable_id("scope", self.canonical())
        if self.scope_id and self.scope_id != expected:
            raise ValueError("registry scope identity mismatch")

@dataclass(frozen=True, slots=True)
class ModelEvidenceBundle:
    bundle_id: str
    model_id: str
    model_version: str
    model_artifact_hash: str
    transform_hash: str
    calibration_hash: str
    feature_schema_hash: str
    label_contract_hash: str
    dataset_hash: str
    training_plan_hash: str
    training_report_hash: str
    model_card_hash: str
    prediction_rowset_hash: str
    anti_overfit_report_hash: str
    phase12_promotion_decision_hash: str
    code_revision: str
    artifact_inventory_hash: str
    attestation_hash: str
    created_at_utc_msc: int
    no_execution_authority: bool = True
    bundle_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/model_evidence_bundle@1.0.0",
            self.bundle_id, self.model_id, self.model_version, self.model_artifact_hash,
            self.transform_hash, self.calibration_hash, self.feature_schema_hash,
            self.label_contract_hash, self.dataset_hash, self.training_plan_hash,
            self.training_report_hash, self.model_card_hash, self.prediction_rowset_hash,
            self.anti_overfit_report_hash, self.phase12_promotion_decision_hash,
            self.code_revision, self.artifact_inventory_hash, self.attestation_hash,
            self.created_at_utc_msc, cbool(self.no_execution_authority)]))

    def with_hash(self) -> "ModelEvidenceBundle":
        return replace(self, bundle_hash=stable_id("mevb", self.canonical()))

    def validate(self) -> None:
        _required(self.bundle_id, self.model_id, self.model_version, self.model_artifact_hash,
                  self.transform_hash, self.calibration_hash, self.feature_schema_hash,
                  self.label_contract_hash, self.dataset_hash, self.training_plan_hash,
                  self.training_report_hash, self.model_card_hash, self.prediction_rowset_hash,
                  self.anti_overfit_report_hash, self.phase12_promotion_decision_hash,
                  self.code_revision, self.artifact_inventory_hash)
        if self.created_at_utc_msc < 0:
            raise ValueError("invalid evidence timestamp")
        if not self.no_execution_authority:
            raise ValueError("Phase 14 evidence cannot carry execution authority")
        expected = stable_id("mevb", self.canonical())
        if self.bundle_hash and self.bundle_hash != expected:
            raise ValueError("model evidence bundle hash mismatch")

@dataclass(frozen=True, slots=True)
class PromotionPolicy:
    policy_id: str
    policy_version: str
    min_test_samples: int
    min_validation_score: float
    min_test_score: float
    max_generalization_gap: float
    max_calibration_error: float
    min_stress_pass_ratio: float
    require_phase12_acceptance: bool = True
    require_test_oos_only: bool = True
    require_lineage_valid: bool = True
    require_inventory_valid: bool = True
    require_model_card_no_capital_authority: bool = True
    require_verified_attestation: bool = False
    max_challengers_per_scope: int = 4
    policy_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/promotion_policy@1.0.0", self.policy_id,
            self.policy_version, self.min_test_samples, cfloat(self.min_validation_score),
            cfloat(self.min_test_score), cfloat(self.max_generalization_gap),
            cfloat(self.max_calibration_error), cfloat(self.min_stress_pass_ratio),
            cbool(self.require_phase12_acceptance), cbool(self.require_test_oos_only),
            cbool(self.require_lineage_valid), cbool(self.require_inventory_valid),
            cbool(self.require_model_card_no_capital_authority), cbool(self.require_verified_attestation),
            self.max_challengers_per_scope]))

    def with_hash(self) -> "PromotionPolicy":
        return replace(self, policy_hash=stable_id("ppol", self.canonical()))

    def validate(self) -> None:
        _required(self.policy_id, self.policy_version)
        if self.min_test_samples <= 0:
            raise ValueError("minimum test sample count must be positive")
        if self.max_generalization_gap < 0 or self.max_calibration_error < 0:
            raise ValueError("gap and calibration bounds must be nonnegative")
        if not 0.0 <= self.min_stress_pass_ratio <= 1.0:
            raise ValueError("stress pass ratio outside unit interval")
        if self.max_challengers_per_scope < 1 or self.max_challengers_per_scope > 64:
            raise ValueError("challenger bound outside supported range")
        expected = stable_id("ppol", self.canonical())
        if self.policy_hash and self.policy_hash != expected:
            raise ValueError("promotion policy hash mismatch")

@dataclass(frozen=True, slots=True)
class PromotionMeasurements:
    phase12_accepted: bool
    test_oos_only: bool
    test_sample_count: int
    validation_score: float
    test_score: float
    calibration_error: float
    stress_pass_ratio: float
    lineage_valid: bool
    inventory_valid: bool
    model_card_no_capital_authority: bool
    attestation_verified: bool

    def validate(self) -> None:
        if self.test_sample_count < 0:
            raise ValueError("negative test sample count")
        for value in (self.validation_score, self.test_score, self.calibration_error, self.stress_pass_ratio):
            if not math.isfinite(value):
                raise ValueError("non-finite promotion measurement")
        if not 0.0 <= self.stress_pass_ratio <= 1.0:
            raise ValueError("stress pass ratio outside unit interval")

@dataclass(frozen=True, slots=True)
class PromotionGateResult:
    gate_id: str
    status: GateStatus
    observed_value: str
    required_value: str
    reason_code: str
    evidence_hash: str
    gate_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/promotion_gate_result@1.0.0",
            self.gate_id, int(self.status), self.observed_value, self.required_value,
            self.reason_code, self.evidence_hash]))

    def with_hash(self) -> "PromotionGateResult":
        return replace(self, gate_hash=stable_id("pgate", self.canonical()))

@dataclass(frozen=True, slots=True)
class PromotionEvaluation:
    evaluation_id: str
    model_artifact_hash: str
    scope_id: str
    evidence_bundle_hash: str
    policy_hash: str
    gates: tuple[PromotionGateResult, ...]
    verdict: PromotionVerdict
    evaluated_at_utc_msc: int
    evaluator_id: str
    no_execution_authority: bool = True
    evaluation_hash: str = ""

    def canonical(self) -> str:
        gate_root = sha256_lines(g.gate_hash or g.with_hash().gate_hash for g in self.gates)
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/promotion_evaluation@1.0.0",
            self.evaluation_id, self.model_artifact_hash, self.scope_id,
            self.evidence_bundle_hash, self.policy_hash, gate_root, int(self.verdict),
            self.evaluated_at_utc_msc, self.evaluator_id, cbool(self.no_execution_authority)]))

    def with_hash(self) -> "PromotionEvaluation":
        gates = tuple(g if g.gate_hash else g.with_hash() for g in self.gates)
        candidate = replace(self, gates=gates, evaluation_hash="")
        return replace(candidate, evaluation_hash=stable_id("peval", candidate.canonical()))

    def validate(self) -> None:
        _required(self.evaluation_id, self.model_artifact_hash, self.scope_id,
                  self.evidence_bundle_hash, self.policy_hash, self.evaluator_id)
        if not self.gates:
            raise ValueError("promotion evaluation requires gates")
        for gate in self.gates:
            expected = gate.with_hash().gate_hash
            if gate.gate_hash and gate.gate_hash != expected:
                raise ValueError("promotion gate hash mismatch")
        has_fail = any(g.status == GateStatus.FAIL for g in self.gates)
        if self.verdict == PromotionVerdict.ELIGIBLE and has_fail:
            raise ValueError("eligible verdict cannot contain failed gates")
        if self.verdict == PromotionVerdict.INELIGIBLE and not has_fail:
            raise ValueError("ineligible verdict requires at least one failed gate")
        if not self.no_execution_authority:
            raise ValueError("Phase 14 evaluation cannot grant execution authority")
        expected = self.with_hash().evaluation_hash
        if self.evaluation_hash and self.evaluation_hash != expected:
            raise ValueError("promotion evaluation hash mismatch")

@dataclass(frozen=True, slots=True)
class ModelRegistryEntry:
    entry_id: str
    model_id: str
    model_version: str
    model_artifact_hash: str
    scope_id: str
    evidence_bundle_hash: str
    evaluation_hash: str
    state: RegistryState
    revision: int
    created_at_utc_msc: int
    updated_at_utc_msc: int
    supersedes_entry_id: str = ""
    no_execution_authority: bool = True
    entry_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/model_registry_entry@1.0.0",
            self.entry_id, self.model_id, self.model_version, self.model_artifact_hash,
            self.scope_id, self.evidence_bundle_hash, self.evaluation_hash, int(self.state),
            self.revision, self.created_at_utc_msc, self.updated_at_utc_msc,
            self.supersedes_entry_id, cbool(self.no_execution_authority)]))

    def with_hash(self) -> "ModelRegistryEntry":
        return replace(self, entry_hash=stable_id("mreg", self.canonical()))

    def validate(self) -> None:
        _required(self.entry_id, self.model_id, self.model_version, self.model_artifact_hash,
                  self.scope_id, self.evidence_bundle_hash)
        if self.revision < 1 or self.updated_at_utc_msc < self.created_at_utc_msc:
            raise ValueError("invalid registry revision or timestamps")
        if not self.no_execution_authority:
            raise ValueError("Phase 14 registry entry cannot carry execution authority")
        if self.state in (RegistryState.EVIDENCE_VALIDATED, RegistryState.CANDIDATE,
                          RegistryState.CHALLENGER, RegistryState.CHAMPION) and not self.evaluation_hash:
            raise ValueError("governed state requires a promotion evaluation")
        expected = stable_id("mreg", self.canonical())
        if self.entry_hash and self.entry_hash != expected:
            raise ValueError("registry entry hash mismatch")

@dataclass(frozen=True, slots=True)
class GovernanceDecision:
    sequence: int
    decision_type: GovernanceDecisionType
    entry_id: str
    scope_id: str
    from_state: RegistryState
    to_state: RegistryState
    actor_id: str
    reason_code: str
    evidence_hash: str
    previous_decision_hash: str
    decided_at_utc_msc: int
    decision_id: str = ""
    decision_hash: str = ""

    def canonical_identity(self) -> str:
        return "|".join(map(str, [self.sequence, int(self.decision_type), self.entry_id,
            self.scope_id, int(self.from_state), int(self.to_state), self.decided_at_utc_msc]))

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/governance_decision@1.0.0",
            self.decision_id, self.canonical_identity(), self.actor_id, self.reason_code,
            self.evidence_hash, self.previous_decision_hash]))

    def with_hashes(self) -> "GovernanceDecision":
        did = self.decision_id or stable_id("gdec", self.canonical_identity())
        candidate = replace(self, decision_id=did, decision_hash="")
        return replace(candidate, decision_hash=stable_id("gdech", candidate.canonical()))

    def validate(self) -> None:
        _required(self.entry_id, self.scope_id, self.actor_id, self.reason_code, self.evidence_hash)
        if self.sequence < 1 or self.decided_at_utc_msc < 0:
            raise ValueError("invalid governance sequence or timestamp")
        expected = self.with_hashes()
        if self.decision_id and self.decision_id != expected.decision_id:
            raise ValueError("governance decision identity mismatch")
        if self.decision_hash and self.decision_hash != expected.decision_hash:
            raise ValueError("governance decision hash mismatch")

@dataclass(frozen=True, slots=True)
class RegistrySnapshot:
    snapshot_id: str
    registry_version: str
    decision_sequence: int
    decision_chain_hash: str
    entry_hashes: tuple[str, ...]
    champion_entry_ids: tuple[str, ...]
    challenger_entry_ids: tuple[str, ...]
    generated_at_utc_msc: int
    no_execution_authority: bool = True
    snapshot_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/registry_snapshot@1.0.0",
            self.snapshot_id, self.registry_version, self.decision_sequence,
            self.decision_chain_hash, sha256_lines(self.entry_hashes),
            sha256_lines(self.champion_entry_ids), sha256_lines(self.challenger_entry_ids),
            self.generated_at_utc_msc, cbool(self.no_execution_authority)]))

    def with_hash(self) -> "RegistrySnapshot":
        return replace(self, snapshot_hash=stable_id("rsnap", self.canonical()))

    def validate(self) -> None:
        _required(self.snapshot_id, self.registry_version, self.decision_chain_hash)
        if self.decision_sequence < 0:
            raise ValueError("negative registry decision sequence")
        if len(set(self.entry_hashes)) != len(self.entry_hashes):
            raise ValueError("duplicate registry entry hashes")
        if not self.no_execution_authority:
            raise ValueError("Phase 14 snapshot cannot carry execution authority")
        expected = stable_id("rsnap", self.canonical())
        if self.snapshot_hash and self.snapshot_hash != expected:
            raise ValueError("registry snapshot hash mismatch")

@dataclass(frozen=True, slots=True)
class RollbackPlan:
    plan_id: str
    scope_id: str
    from_entry_id: str
    to_entry_id: str
    trigger_codes: tuple[str, ...]
    registry_snapshot_hash: str
    approved_by: str
    approved_at_utc_msc: int
    no_execution_authority: bool = True
    plan_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/rollback_plan@1.0.0", self.plan_id,
            self.scope_id, self.from_entry_id, self.to_entry_id, "||".join(self.trigger_codes),
            self.registry_snapshot_hash, self.approved_by, self.approved_at_utc_msc,
            cbool(self.no_execution_authority)]))

    def with_hash(self) -> "RollbackPlan":
        return replace(self, plan_hash=stable_id("rplan", self.canonical()))

    def validate(self) -> None:
        _required(self.plan_id, self.scope_id, self.from_entry_id, self.to_entry_id,
                  self.registry_snapshot_hash, self.approved_by)
        if self.from_entry_id == self.to_entry_id:
            raise ValueError("rollback source and target must differ")
        if not self.trigger_codes or len(set(self.trigger_codes)) != len(self.trigger_codes):
            raise ValueError("rollback triggers must be nonempty and unique")
        if not self.no_execution_authority:
            raise ValueError("Phase 14 rollback plan cannot execute capital actions")
        expected = stable_id("rplan", self.canonical())
        if self.plan_hash and self.plan_hash != expected:
            raise ValueError("rollback plan hash mismatch")

@dataclass(frozen=True, slots=True)
class ModelReleaseManifest:
    release_id: str
    release_version: str
    channel: ReleaseChannel
    registry_snapshot_hash: str
    registry_entry_hash: str
    model_artifact_hash: str
    transform_hash: str
    calibration_hash: str
    feature_schema_hash: str
    label_contract_hash: str
    artifact_inventory_hash: str
    attestation_hash: str
    created_at_utc_msc: int
    no_execution_authority: bool = True
    release_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/model_release_manifest@1.0.0",
            self.release_id, self.release_version, int(self.channel), self.registry_snapshot_hash,
            self.registry_entry_hash, self.model_artifact_hash, self.transform_hash,
            self.calibration_hash, self.feature_schema_hash, self.label_contract_hash,
            self.artifact_inventory_hash, self.attestation_hash, self.created_at_utc_msc,
            cbool(self.no_execution_authority)]))

    def with_hash(self) -> "ModelReleaseManifest":
        return replace(self, release_hash=stable_id("mrel", self.canonical()))

    def validate(self) -> None:
        _required(self.release_id, self.release_version, self.registry_snapshot_hash,
                  self.registry_entry_hash, self.model_artifact_hash, self.transform_hash,
                  self.feature_schema_hash, self.label_contract_hash, self.artifact_inventory_hash)
        if self.channel == ReleaseChannel.SHADOW_ELIGIBLE and not self.attestation_hash:
            raise ValueError("shadow-eligible release requires authenticity attestation")
        if not self.no_execution_authority:
            raise ValueError("Phase 14 release manifest cannot grant execution authority")
        expected = stable_id("mrel", self.canonical())
        if self.release_hash and self.release_hash != expected:
            raise ValueError("model release hash mismatch")

@dataclass(frozen=True, slots=True)
class GovernanceReportManifest:
    report_id: str
    evidence_bundle_hash: str
    promotion_evaluation_hash: str
    registry_snapshot_hash: str
    release_manifest_hash: str
    rollback_plan_hash: str
    decision_chain_hash: str
    generated_at_utc_msc: int
    report_hash: str = ""

    def canonical(self) -> str:
        return "|".join(map(str, [f"{SCHEMA_PREFIX}/governance_report_manifest@1.0.0",
            self.report_id, self.evidence_bundle_hash, self.promotion_evaluation_hash,
            self.registry_snapshot_hash, self.release_manifest_hash, self.rollback_plan_hash,
            self.decision_chain_hash, self.generated_at_utc_msc]))

    def with_hash(self) -> "GovernanceReportManifest":
        return replace(self, report_hash=stable_id("grep", self.canonical()))
