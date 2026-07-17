from __future__ import annotations
from dataclasses import dataclass
from .identity import artifact_base
from .semver import Version
from .types import Reason

@dataclass(frozen=True,slots=True)
class MigrationPlan:
    migration_id:str
    artifact_base_id:str
    from_version:str
    to_version:str
    migration_artifact_id:str
    rollback_artifact_id:str
    idempotency_key:str
    dry_run_supported:bool
    dual_read_required:bool
    irreversible:bool
    authority_decision_ref:str

class MigrationRegistry:
    def __init__(self,policies): self.policy=policies.documents["migration_policy"]
    def validate(self,plans:list[MigrationPlan])->list[Reason]:
        reasons=[]; ids=set(); pairs=set(); graph={}
        for p in plans:
            if p.migration_id in ids: reasons.append(Reason("MIGRATION_ID_DUPLICATE","Migration ID is duplicated.",{"migration_id":p.migration_id}))
            ids.add(p.migration_id)
            pair=(p.artifact_base_id,p.from_version,p.to_version)
            if pair in pairs: reasons.append(Reason("MIGRATION_PATH_DUPLICATE","Migration path is duplicated.",{"path":list(pair)}))
            pairs.add(pair)
            fv,tv=Version.parse(p.from_version),Version.parse(p.to_version)
            if tv.precedence_key()<=fv.precedence_key(): reasons.append(Reason("MIGRATION_NOT_FORWARD","Migration target must be newer than source.",{}))
            if not p.idempotency_key: reasons.append(Reason("MIGRATION_IDEMPOTENCY_MISSING","Migration requires an idempotency key.",{}))
            if not p.dry_run_supported: reasons.append(Reason("MIGRATION_DRY_RUN_REQUIRED","Migration must support dry-run.",{}))
            if p.irreversible and not self.policy.get("allow_irreversible",False): reasons.append(Reason("IRREVERSIBLE_MIGRATION_DENIED","Irreversible migrations are denied by policy.",{}))
            if not p.rollback_artifact_id: reasons.append(Reason("MIGRATION_ROLLBACK_MISSING","Migration requires rollback artifact.",{}))
            if not p.authority_decision_ref: reasons.append(Reason("MIGRATION_AUTHORITY_MISSING","Migration requires ACL-00 authority decision.",{}))
            graph.setdefault((p.artifact_base_id,p.from_version),[]).append(p.to_version)
        return reasons
