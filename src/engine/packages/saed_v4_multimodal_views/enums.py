from enum import Enum
class ViewKind(str,Enum):
    PRICE='price'; STRUCTURE='structure'; TIME='time'; HIGHER_TIMEFRAME='higher_timeframe'; INTERMARKET='intermarket'; LIQUIDITY='liquidity'; SESSION='session'; EXECUTION='execution'; CONTEXT_ANCESTRY='context_ancestry'; TREATMENT_DESCRIPTOR='treatment_descriptor'; CUSTOM='custom'
class FeatureType(str,Enum): NUMBER='number'; STRING='string'; BOOLEAN='boolean'; VECTOR='vector'; CATEGORY='category'
class MissingnessPolicy(str,Enum): PROHIBIT='prohibit'; MASK='mask'; UNKNOWN='unknown'; EXPLICIT_DEFAULT='explicit_default'
class NormalizationKind(str,Enum): NONE='none'; STATIC_ZSCORE='static_zscore'; STATIC_ROBUST='static_robust'; STATIC_MINMAX='static_minmax'
class TransformKind(str,Enum): IDENTITY='identity'; MIDPOINT='midpoint'; SPREAD='spread'; DIFFERENCE='difference'; RATIO='ratio'; LOG_RETURN='log_return'; BOOLEAN_AND='boolean_and'; BOOLEAN_OR='boolean_or'; CONCAT='concat'; VECTOR='vector'; AGE_SECONDS='age_seconds'
class ViewStatus(str,Enum): COMPLETE='complete'; DEGRADED='degraded'; UNKNOWN='unknown'; CONFLICTED='conflicted'; QUARANTINED='quarantined'
class SupportStatus(str,Enum): SUPPORTED='supported'; DEGRADED='degraded'; UNSUPPORTED='unsupported'; UNKNOWN='unknown'
class CompatibilityStatus(str,Enum): COMPATIBLE='compatible'; DEGRADED='degraded'; INCOMPATIBLE='incompatible'
class EvidenceRole(str,Enum): DEVELOPMENT='development'; CALIBRATION='calibration'; SELECTION_VALIDATION='selection_validation'; LOCKED_FINAL='locked_final'; PROSPECTIVE='prospective'; SHADOW='shadow'; MICRO_LIVE='micro_live'; LIVE='live'; SYNTHETIC_STRESS='synthetic_stress'; EXTERNAL_STATIC='external_static'; EXTERNAL_ACTUAL='external_actual'
