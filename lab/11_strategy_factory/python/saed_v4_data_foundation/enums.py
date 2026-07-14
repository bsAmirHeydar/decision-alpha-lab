from enum import Enum
class DataRole(str,Enum):
    DEVELOPMENT='development'; CALIBRATION='calibration'; SELECTION_VALIDATION='selection_validation'; LOCKED_FINAL='locked_final'; PROSPECTIVE='prospective'; SHADOW='shadow'; MICRO_LIVE='micro_live'; LIVE='live'; SYNTHETIC_STRESS='synthetic_stress'; EXTERNAL_STATIC='external_static'; EXTERNAL_ACTUAL='external_actual'
class ArtifactKind(str,Enum):
    RAW_EVENT='raw_event'; CANONICAL_RECORD='canonical_record'; REVISION='revision'; DATASET_SNAPSHOT='dataset_snapshot'; FEATURE_SNAPSHOT='feature_snapshot'; SEQUENCE_SNAPSHOT='sequence_snapshot'; GRAPH_SNAPSHOT='graph_snapshot'; PATH_SNAPSHOT='path_snapshot'; EMBEDDING_SNAPSHOT='embedding_snapshot'; EVIDENCE_BUNDLE='evidence_bundle'; TWIN_SEED='twin_seed'
class ArtifactState(str,Enum):
    PROPOSED='proposed'; VERIFIED='verified'; QUARANTINED='quarantined'; RETIRED='retired'
class IntegrityStatus(str,Enum):
    PASS='pass'; FAIL='fail'; UNKNOWN='unknown'
class SchemaCompatibility(str,Enum):
    EXACT='exact'; DECLARED_MIGRATION='declared_migration'; INCOMPATIBLE='incompatible'
class QuarantineReason(str,Enum):
    SCHEMA_INVALID='schema_invalid'; TEMPORAL_INVALID='temporal_invalid'; HASH_CONFLICT='hash_conflict'; DUPLICATE_CONFLICT='duplicate_conflict'; LINEAGE_INVALID='lineage_invalid'; ROLE_VIOLATION='role_violation'; SOURCE_UNTRUSTED='source_untrusted'; MANUAL_HOLD='manual_hold'
class RetentionClass(str,Enum):
    TRANSIENT='transient'; RESEARCH='research'; EVIDENCE='evidence'; REGULATED='regulated'; PERMANENT='permanent'
class AccessOperation(str,Enum):
    READ='read'; WRITE='write'; TRAIN='train'; TUNE='tune'; CALIBRATE='calibrate'; SELECT='select'; REPORT='report'; PROMOTE='promote'; REPLAY='replay'; DELETE='delete'
class LineageEdgeType(str,Enum):
    DERIVED_FROM='derived_from'; SUPERSEDES='supersedes'; CALIBRATED_FROM='calibrated_from'; SELECTED_FROM='selected_from'; PACKAGED_FROM='packaged_from'; MIGRATED_FROM='migrated_from'
