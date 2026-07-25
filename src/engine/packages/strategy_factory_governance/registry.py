from __future__ import annotations
from dataclasses import replace
from .models import *
from .enums import *
from .ledger import AppendOnlyDecisionLedger
from .hashing import stable_id

_ALLOWED={
 RegistryState.DRAFT:{RegistryState.REGISTERED,RegistryState.REJECTED},
 RegistryState.REGISTERED:{RegistryState.EVIDENCE_VALIDATED,RegistryState.REJECTED},
 RegistryState.EVIDENCE_VALIDATED:{RegistryState.CANDIDATE,RegistryState.REJECTED},
 RegistryState.CANDIDATE:{RegistryState.CHALLENGER,RegistryState.REJECTED,RegistryState.RETIRED},
 RegistryState.CHALLENGER:{RegistryState.CHAMPION,RegistryState.SUSPENDED,RegistryState.RETIRED,RegistryState.REJECTED},
 RegistryState.CHAMPION:{RegistryState.SUSPENDED,RegistryState.RETIRED},
 RegistryState.SUSPENDED:{RegistryState.CHALLENGER,RegistryState.RETIRED,RegistryState.REJECTED},
 RegistryState.RETIRED:set(), RegistryState.REJECTED:set(),
}

class ModelRegistry:
    def __init__(self, *, registry_version="1.0.0", max_entries=256, max_decisions=4096):
        self.registry_version=registry_version
        self.max_entries=max_entries
        self.max_decisions=max_decisions
        self._entries={}
        self._history={}
        self.ledger=AppendOnlyDecisionLedger()

    @property
    def entries(self):
        return tuple(sorted(self._entries.values(), key=lambda e:e.entry_id))

    def get(self, entry_id):
        try:return self._entries[entry_id]
        except KeyError as exc:raise KeyError(f"unknown registry entry: {entry_id}") from exc

    def history(self, entry_id):
        return tuple(self._history.get(entry_id,()))

    def champion_for_scope(self, scope_id):
        matches=[e for e in self._entries.values() if e.scope_id==scope_id and e.state==RegistryState.CHAMPION]
        if len(matches)>1:raise RuntimeError("registry invariant violation: multiple champions")
        return matches[0] if matches else None

    def challengers_for_scope(self, scope_id):
        return tuple(sorted((e for e in self._entries.values() if e.scope_id==scope_id and e.state==RegistryState.CHALLENGER), key=lambda e:e.entry_id))

    def _store(self, entry):
        entry.validate(); entry=entry if entry.entry_hash else entry.with_hash()
        self._entries[entry.entry_id]=entry
        self._history.setdefault(entry.entry_id,[]).append(entry)
        return entry

    def _decision(self, entry, *, dtype, from_state, to_state, actor_id, reason_code,
                  evidence_hash, at):
        if len(self.ledger.decisions)>=self.max_decisions:raise OverflowError("governance ledger capacity exceeded")
        d=GovernanceDecision(len(self.ledger.decisions)+1,dtype,entry.entry_id,entry.scope_id,
            from_state,to_state,actor_id,reason_code,evidence_hash,self.ledger.last_hash,at)
        return self.ledger.append(d)

    def register(self, *, model_id, model_version, model_artifact_hash, scope_id,
                 evidence_bundle_hash, created_at_utc_msc, actor_id="registry", reason_code="REGISTERED"):
        if len(self._entries)>=self.max_entries:raise OverflowError("model registry capacity exceeded")
        if any(e.model_id==model_id and e.model_version==model_version and e.scope_id==scope_id for e in self._entries.values()):
            raise ValueError("duplicate exact model version in registry scope")
        entry_id=stable_id("mentry", "|".join([model_id,model_version,model_artifact_hash,scope_id]))
        entry=ModelRegistryEntry(entry_id,model_id,model_version,model_artifact_hash,scope_id,
            evidence_bundle_hash,"",RegistryState.REGISTERED,1,created_at_utc_msc,
            created_at_utc_msc).with_hash()
        self._store(entry)
        self._decision(entry,dtype=GovernanceDecisionType.REGISTER,from_state=RegistryState.DRAFT,
            to_state=RegistryState.REGISTERED,actor_id=actor_id,reason_code=reason_code,
            evidence_hash=evidence_bundle_hash,at=created_at_utc_msc)
        return entry

    def transition(self, entry_id, to_state, *, decision_type, actor_id, reason_code,
                   evidence_hash, at, evaluation=None, supersedes_entry_id=""):
        current=self.get(entry_id)
        if to_state not in _ALLOWED[current.state]:
            raise ValueError(f"invalid registry transition {current.state.name}->{to_state.name}")
        eval_hash=current.evaluation_hash
        if evaluation is not None:
            evaluation.validate()
            if evaluation.model_artifact_hash!=current.model_artifact_hash or evaluation.scope_id!=current.scope_id:
                raise ValueError("promotion evaluation does not belong to registry entry")
            eval_hash=evaluation.evaluation_hash
        if to_state in (RegistryState.EVIDENCE_VALIDATED,RegistryState.CANDIDATE,
                        RegistryState.CHALLENGER,RegistryState.CHAMPION):
            if evaluation is None and not eval_hash:
                raise ValueError("governed registry transition requires evaluation evidence")
            if evaluation is not None and evaluation.verdict!=PromotionVerdict.ELIGIBLE:
                raise ValueError("ineligible model cannot enter a promotable state")
        updated=replace(current,state=to_state,revision=current.revision+1,
                        updated_at_utc_msc=at,evaluation_hash=eval_hash,
                        supersedes_entry_id=supersedes_entry_id or current.supersedes_entry_id,
                        entry_hash="").with_hash()
        updated.validate(); self._store(updated)
        self._decision(updated,dtype=decision_type,from_state=current.state,to_state=to_state,
            actor_id=actor_id,reason_code=reason_code,evidence_hash=evidence_hash,at=at)
        return updated

    def validate_evidence(self, entry_id, evaluation, *, actor_id="promotion_engine", at=0):
        return self.transition(entry_id,RegistryState.EVIDENCE_VALIDATED,
            decision_type=GovernanceDecisionType.VALIDATE_EVIDENCE,actor_id=actor_id,
            reason_code="EVIDENCE_VALIDATED",evidence_hash=evaluation.evaluation_hash,at=at,
            evaluation=evaluation)

    def nominate(self, entry_id, *, actor_id="promotion_engine", at=0):
        return self.transition(entry_id,RegistryState.CANDIDATE,
            decision_type=GovernanceDecisionType.NOMINATE_CANDIDATE,actor_id=actor_id,
            reason_code="CANDIDATE_NOMINATED",evidence_hash=self.get(entry_id).evaluation_hash,at=at)

    def assign_challenger(self, entry_id, policy, *, actor_id="governance", at=0):
        current=self.get(entry_id)
        if len(self.challengers_for_scope(current.scope_id))>=policy.max_challengers_per_scope:
            raise ValueError("challenger capacity reached for scope")
        return self.transition(entry_id,RegistryState.CHALLENGER,
            decision_type=GovernanceDecisionType.ASSIGN_CHALLENGER,actor_id=actor_id,
            reason_code="CHALLENGER_ASSIGNED",evidence_hash=current.evaluation_hash,at=at)

    def promote_champion(self, entry_id, *, actor_id="governance", at=0):
        candidate=self.get(entry_id)
        current_champion=self.champion_for_scope(candidate.scope_id)
        if current_champion and current_champion.entry_id==entry_id:return current_champion
        if current_champion:
            self.transition(current_champion.entry_id,RegistryState.RETIRED,
                decision_type=GovernanceDecisionType.SUPERSEDE,actor_id=actor_id,
                reason_code="SUPERSEDED_BY_NEW_CHAMPION",evidence_hash=candidate.evaluation_hash,
                at=at,supersedes_entry_id="")
        promoted=self.transition(entry_id,RegistryState.CHAMPION,
            decision_type=GovernanceDecisionType.PROMOTE_CHAMPION,actor_id=actor_id,
            reason_code="CHAMPION_PROMOTED",evidence_hash=candidate.evaluation_hash,at=at,
            supersedes_entry_id=current_champion.entry_id if current_champion else "")
        if len([e for e in self._entries.values() if e.scope_id==candidate.scope_id and e.state==RegistryState.CHAMPION])!=1:
            raise RuntimeError("champion uniqueness invariant failed")
        return promoted

    def suspend(self, entry_id, reason_code, *, actor_id="governance", at=0):
        return self.transition(entry_id,RegistryState.SUSPENDED,
            decision_type=GovernanceDecisionType.SUSPEND,actor_id=actor_id,
            reason_code=reason_code,evidence_hash=self.get(entry_id).entry_hash,at=at)

    def retire(self, entry_id, reason_code="RETIRED", *, actor_id="governance", at=0):
        return self.transition(entry_id,RegistryState.RETIRED,
            decision_type=GovernanceDecisionType.RETIRE,actor_id=actor_id,
            reason_code=reason_code,evidence_hash=self.get(entry_id).entry_hash,at=at)

    def rollback(self, plan, *, actor_id="governance", at=0):
        plan.validate()
        current=self.champion_for_scope(plan.scope_id)
        if current is None or current.entry_id!=plan.from_entry_id:
            raise ValueError("rollback source is not current champion")
        target=self.get(plan.to_entry_id)
        if target.scope_id!=plan.scope_id or target.state not in (RegistryState.CHALLENGER,RegistryState.SUSPENDED):
            raise ValueError("rollback target is not an eligible prior model")
        self.transition(current.entry_id,RegistryState.RETIRED,
            decision_type=GovernanceDecisionType.ROLLBACK,actor_id=actor_id,
            reason_code="ROLLBACK_SOURCE_RETIRED",evidence_hash=plan.plan_hash,at=at)
        if target.state==RegistryState.SUSPENDED:
            target=self.transition(target.entry_id,RegistryState.CHALLENGER,
                decision_type=GovernanceDecisionType.RESTORE_CHALLENGER,actor_id=actor_id,
                reason_code="ROLLBACK_TARGET_RESTORED",evidence_hash=plan.plan_hash,at=at)
        return self.transition(target.entry_id,RegistryState.CHAMPION,
            decision_type=GovernanceDecisionType.ROLLBACK,actor_id=actor_id,
            reason_code="ROLLBACK_TARGET_PROMOTED",evidence_hash=plan.plan_hash,at=at,
            supersedes_entry_id=current.entry_id)
