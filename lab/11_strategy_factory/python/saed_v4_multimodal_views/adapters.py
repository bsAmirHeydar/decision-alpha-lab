from __future__ import annotations
from .models import SourceValue
from .enums import EvidenceRole
from .canonical import content_hash

def projection_sources(projection,evidence_role=EvidenceRole.DEVELOPMENT,namespace='projection'):
    values=[]
    for item in projection.values:
        if item.missing:continue
        values.append(SourceValue(namespace,item.field_id,item.value,item.last_event_time or projection.event_as_of,projection.known_as_of,0.0 if item.missing else 1.0,evidence_role,projection.projection_id,projection.state_hash,tuple(item.event_ids)))
    return tuple(values)

def mapping_sources(namespace,mapping,event_time,known_time,evidence_role,artifact_id,artifact_hash,quality=1.0):
    return tuple(SourceValue(namespace,str(k),v,event_time,known_time,float(quality),evidence_role,artifact_id,artifact_hash) for k,v in sorted(mapping.items()))

def source_hash_for_mapping(mapping):return content_hash(mapping)
