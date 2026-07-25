from dataclasses import dataclass
from .canonical import canonical_sha256
from .constants import *
@dataclass(frozen=True,slots=True)
class ContractDescriptor:
    name:str;version:str;identity_prefix:str;authority:str
CATALOG=(
 ContractDescriptor('WindowStoreConfig',PHASE_VERSION,'FPCFG','NONE'),ContractDescriptor('WindowDescriptor',PHASE_VERSION,'FPWINDESC','NONE'),ContractDescriptor('SymbolWindowAggregate',PHASE_VERSION,'FPSYM_WINDOW','NONE'),ContractDescriptor('PairWindowAggregate',PHASE_VERSION,'FPPAIR_WINDOW','NONE'),ContractDescriptor('CalendarDaySelectionItem',PHASE_VERSION,'FP_N_ITEM','NONE'),ContractDescriptor('CalendarDaySelection',PHASE_VERSION,'FP_N_SELECTOR','NONE'),ContractDescriptor('ReferenceLevel',PHASE_VERSION,'FPREF','NONE'),ContractDescriptor('ReferenceTransitionRecord',PHASE_VERSION,'FPREFEVT','NONE'),ContractDescriptor('ReferenceSet',PHASE_VERSION,'FPREFSET','NONE'),ContractDescriptor('WindowStoreSnapshot',PHASE_VERSION,'FPSTORE','NONE'),ContractDescriptor('RevisionInvalidation',PHASE_VERSION,'FPINVALIDATE','NONE'),ContractDescriptor('WindowStoreCheckpoint',PHASE_VERSION,'FPCHECKPOINT','NONE'))
def registry_hash():return canonical_sha256(CATALOG)
