from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .models import SovereignRecord,QuarantineRecord
from .schema_registry import SchemaRegistry
from .revisions import RevisionStore
from .quarantine import QuarantineRegistry
from .canonical import stable_id,content_hash
from .enums import QuarantineReason
from .errors import DataFoundationError
@dataclass(frozen=True)
class IngestionResult:
    accepted_revision_ids:tuple[str,...]; quarantined_ids:tuple[str,...]; batch_id:str
class IngestionEngine:
    def __init__(self,schemas:SchemaRegistry,revisions:RevisionStore,quarantine:QuarantineRegistry): self.schemas=schemas; self.revisions=revisions; self.quarantine=quarantine
    def ingest_atomic(self,records:Iterable[SovereignRecord])->IngestionResult:
        items=tuple(records); planned=[]; failures=[]
        for r in items:
            try:
                self.schemas.validate(r.schema_name,r.schema_version,dict(r.payload)); self.quarantine.require_clear(r.entity_id); planned.append(r)
            except Exception as e: failures.append((r,e))
        if failures:
            qids=[]
            for r,e in failures:
                qid=stable_id('q',{'record':r.to_dict(),'error':type(e).__name__,'message':str(e)})
                reason=QuarantineReason.SCHEMA_INVALID if 'schema' in str(e).lower() or type(e).__name__=='ContractError' else QuarantineReason.MANUAL_HOLD
                self.quarantine.add(QuarantineRecord(qid,r.entity_id,reason,{'error':type(e).__name__,'message':str(e)},content_hash(r.to_dict()))); qids.append(qid)
            return IngestionResult((),tuple(qids),stable_id('batch',{'accepted':[],'quarantined':qids}))
        # preflight revision chains using a shadow plan to prevent partial commits
        heads={entity:(self.revisions.latest(entity).revision_id,len(self.revisions._by_entity[entity])) if self.revisions._by_entity.get(entity) else (None,0) for entity in {r.entity_id for r in planned}}
        for r in planned:
            head,count=heads[r.entity_id]
            if r.revision_number!=count+1 or r.supersedes_revision_id!=head: raise DataFoundationError('atomic preflight failed: invalid revision chain')
            heads[r.entity_id]=(r.revision_id,count+1)
        ids=tuple(self.revisions.append(r) for r in planned)
        return IngestionResult(ids,(),stable_id('batch',{'accepted':ids,'quarantined':[]}))
