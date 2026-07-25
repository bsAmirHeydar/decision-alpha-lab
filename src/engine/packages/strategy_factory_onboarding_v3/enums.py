from enum import Enum
class MigrationWave(str,Enum):A='wave_a';B='wave_b';C='wave_c'
class ContextKind(str,Enum):INTERMARKET='intermarket';STRUCTURAL='structural';CYCLE='cycle';ICT='ict';ASTRO='astro';MANUAL_ONLY='manual_only'
class AdapterMode(str,Enum):SHADOW='shadow';DIFFERENTIAL='differential';CANONICAL='canonical';QUARANTINED='quarantined'
class MigrationStatus(str,Enum):PLANNED='planned';PARITY_PENDING='parity_pending';PARITY_PASSED='parity_passed';MIGRATED='migrated';REJECTED='rejected';STOPPED='stopped'
class CapabilityDecision(str,Enum):ALLOW='allow';DENY='deny';DECLARED_EXCEPTION='declared_exception'
class ParityStatus(str,Enum):PASS='pass';FAIL='fail';INSUFFICIENT='insufficient'
class InvarianceStatus(str,Enum):PASS='pass';FAIL='fail';ADR_REQUIRED='adr_required'
