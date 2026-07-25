from __future__ import annotations
from typing import Iterable
from .models import DatasetSnapshot,SovereignRecord
from .canonical import stable_id,content_hash,merkle_root,normalize_time
from .enums import DataRole
from .partitions import assert_derivation_flow

def build_snapshot(records:Iterable[SovereignRecord],known_as_of:str,event_as_of:str|None,data_role:DataRole,lineage_root:str,metadata=None)->DatasetSnapshot:
    rows=tuple(sorted(records,key=lambda r:(r.entity_id,r.revision_number,r.revision_id)))
    for r in rows: assert_derivation_flow(r.data_role,data_role)
    artifact_ids=tuple(r.revision_id for r in rows); row_ids=tuple(stable_id('row',{'entity_id':r.entity_id,'revision_id':r.revision_id}) for r in rows)
    schema_set_hash=content_hash(sorted({(r.schema_name,r.schema_version) for r in rows}))
    semantic={'artifact_ids':artifact_ids,'row_ids':row_ids,'known_as_of':normalize_time(known_as_of),'event_as_of':normalize_time(event_as_of) if event_as_of else None,'data_role':data_role.value,'schema_set_hash':schema_set_hash,'lineage_root':lineage_root,'record_count':len(rows),'metadata':metadata or {}}
    sid=stable_id('snap',semantic)
    return DatasetSnapshot(sid,artifact_ids,row_ids,semantic['known_as_of'],semantic['event_as_of'],data_role,schema_set_hash,lineage_root,len(rows),metadata or {})
