from __future__ import annotations
from dataclasses import dataclass,field,asdict
from typing import Any,Mapping,Sequence
from .canonical import content_hash,stable_id
from .temporal import BitemporalStamp
from .enums import ArtifactKind,ArtifactState,DataRole,LineageEdgeType,QuarantineReason,RetentionClass
@dataclass(frozen=True)
class SourceDescriptor:
    source_id:str; source_type:str; jurisdiction:str; trust_tier:str; connector_version:str
    def to_dict(self): return asdict(self)
@dataclass(frozen=True)
class SovereignRecord:
    entity_id:str; schema_name:str; schema_version:str; payload:Mapping[str,Any]; temporal:BitemporalStamp; source:SourceDescriptor; data_role:DataRole=DataRole.DEVELOPMENT; revision_number:int=1; supersedes_revision_id:str|None=None
    @property
    def semantic_payload(self):
        return {'entity_id':self.entity_id,'schema_name':self.schema_name,'schema_version':self.schema_version,'payload':dict(self.payload),'temporal':asdict(self.temporal),'source':self.source.to_dict(),'data_role':self.data_role.value,'revision_number':self.revision_number,'supersedes_revision_id':self.supersedes_revision_id}
    @property
    def record_hash(self): return content_hash(self.semantic_payload)
    @property
    def revision_id(self): return stable_id('rev',self.semantic_payload)
    def to_dict(self): return {**self.semantic_payload,'record_hash':self.record_hash,'revision_id':self.revision_id}
@dataclass(frozen=True)
class ArtifactDescriptor:
    artifact_id:str; artifact_kind:ArtifactKind; exact_version:str; content_hash:str; schema_name:str; schema_version:str; data_role:DataRole; state:ArtifactState=ArtifactState.VERIFIED; retention_class:RetentionClass=RetentionClass.EVIDENCE; metadata:Mapping[str,Any]=field(default_factory=dict)
    def semantic_payload(self): return {'artifact_id':self.artifact_id,'artifact_kind':self.artifact_kind.value,'exact_version':self.exact_version,'content_hash':self.content_hash,'schema_name':self.schema_name,'schema_version':self.schema_version,'data_role':self.data_role.value,'state':self.state.value,'retention_class':self.retention_class.value,'metadata':dict(self.metadata)}
    @property
    def descriptor_hash(self): return content_hash(self.semantic_payload())
@dataclass(frozen=True)
class LineageEdge:
    parent_artifact_id:str; child_artifact_id:str; edge_type:LineageEdgeType; transform_id:str; transform_version:str; transform_hash:str
    @property
    def edge_id(self): return stable_id('lin',asdict(self))
@dataclass(frozen=True)
class DatasetSnapshot:
    snapshot_id:str; artifact_ids:tuple[str,...]; row_ids:tuple[str,...]; known_as_of:str; event_as_of:str|None; data_role:DataRole; schema_set_hash:str; lineage_root:str; record_count:int; metadata:Mapping[str,Any]=field(default_factory=dict)
    def semantic_payload(self): return {'snapshot_id':self.snapshot_id,'artifact_ids':list(self.artifact_ids),'row_ids':list(self.row_ids),'known_as_of':self.known_as_of,'event_as_of':self.event_as_of,'data_role':self.data_role.value,'schema_set_hash':self.schema_set_hash,'lineage_root':self.lineage_root,'record_count':self.record_count,'metadata':dict(self.metadata)}
    @property
    def snapshot_hash(self): return content_hash(self.semantic_payload())
@dataclass(frozen=True)
class QuarantineRecord:
    quarantine_id:str; subject_id:str; reason:QuarantineReason; details:Mapping[str,Any]; evidence_hash:str; resolved:bool=False; resolution_hash:str|None=None
@dataclass(frozen=True)
class ReproductionReceipt:
    receipt_id:str; artifact_id:str; expected_hash:str; observed_hash:str; environment_hash:str; exact:bool; details:Mapping[str,Any]=field(default_factory=dict)
@dataclass(frozen=True)
class TwinSeedPackage:
    package_id:str; context_specification_artifact_id:str; snapshot_ids:tuple[str,...]; schema_versions:Mapping[str,str]; lineage_root:str; known_as_of:str; constitution_hash:str; limitations:tuple[str,...]
    @property
    def package_hash(self): return content_hash(asdict(self))
