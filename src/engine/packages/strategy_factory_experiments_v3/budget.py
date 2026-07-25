"""Hierarchical hard-budget accounting for UCE-I11."""

from __future__ import annotations

from dataclasses import asdict, replace

from .canonical import canonical_sha256, stable_id
from .contracts import BudgetAssessment, BudgetPolicy, BudgetUsage, ResourceClaim, WorkResult
from .enums import BudgetDecision


class BudgetManager:
    """Assess and account trial resource claims without hidden oversubscription."""

    def __init__(self, policy: BudgetPolicy) -> None:
        self.policy = policy
        self.usage = BudgetUsage()

    def assess(self, claim: ResourceClaim, candidate_key: str) -> BudgetAssessment:
        reasons: list[str] = []
        usage = self.usage
        if usage.trials_started >= self.policy.max_trials:
            reasons.append("trial_count_exhausted")
        if usage.total_wall_seconds + claim.wall_seconds > self.policy.max_total_wall_seconds:
            reasons.append("total_wall_budget_exhausted")
        if claim.wall_seconds > self.policy.max_trial_wall_seconds:
            reasons.append("trial_wall_budget_exceeded")
        if claim.memory_mb > self.policy.max_memory_mb:
            reasons.append("memory_budget_exceeded")
        if claim.cpu_slots > self.policy.cpu_slots:
            reasons.append("cpu_slot_budget_exceeded")
        if claim.gpu_slots > self.policy.gpu_slots:
            reasons.append("gpu_slot_budget_exceeded")
        if usage.artifact_bytes + claim.artifact_bytes > self.policy.max_artifact_bytes:
            reasons.append("artifact_retention_budget_exhausted")
        if usage.per_candidate_trials.get(candidate_key, 0) >= self.policy.per_candidate_trial_cap:
            reasons.append("candidate_trial_cap_exhausted")
        decision = BudgetDecision.DENY if reasons else BudgetDecision.ALLOW
        payload = {
            "decision": decision.value,
            "reason_codes": reasons,
            "usage_before": asdict(usage),
            "claim_hash": claim.claim_hash,
            "candidate_key": candidate_key,
            "policy_hash": self.policy.policy_hash,
        }
        return BudgetAssessment(
            stable_id("ucebudget", payload),
            decision,
            tuple(reasons),
            usage,
            claim,
            self.policy.policy_hash,
            canonical_sha256(payload),
        )

    def reserve(self, claim: ResourceClaim, candidate_key: str) -> BudgetAssessment:
        assessment = self.assess(claim, candidate_key)
        if assessment.decision is BudgetDecision.DENY:
            return assessment
        per_candidate = dict(self.usage.per_candidate_trials)
        per_candidate[candidate_key] = per_candidate.get(candidate_key, 0) + 1
        self.usage = replace(
            self.usage,
            trials_started=self.usage.trials_started + 1,
            memory_high_water_mb=max(self.usage.memory_high_water_mb, claim.memory_mb),
            per_candidate_trials=per_candidate,
        )
        return assessment

    def complete(self, result: WorkResult) -> None:
        self.usage = replace(
            self.usage,
            trials_completed=self.usage.trials_completed + 1,
            total_wall_seconds=self.usage.total_wall_seconds + result.elapsed_seconds,
            artifact_bytes=self.usage.artifact_bytes + result.artifact_bytes,
        )
