from __future__ import annotations
from fp_i02_kernel.enums import RelationCode,WindowKind
from .contracts import RelationDescriptor
from .enums import RelationFamily
from .canonical import canonical_sha256
from .errors import FPI06Error

CATALOG=(
 RelationDescriptor(RelationCode.AL,RelationFamily.SAME_DAY,WindowKind.A,WindowKind.L,False,False,True,True),
 RelationDescriptor(RelationCode.AN,RelationFamily.SAME_DAY,WindowKind.A,WindowKind.N,False,False,True,True),
 RelationDescriptor(RelationCode.LN,RelationFamily.SAME_DAY,WindowKind.L,WindowKind.N,False,False,True,True),
 RelationDescriptor(RelationCode.NA,RelationFamily.PRIOR_N_CALENDAR_OFFSET,WindowKind.N,WindowKind.A,True,True,True,True),
 RelationDescriptor(RelationCode.NL,RelationFamily.PRIOR_N_CALENDAR_OFFSET,WindowKind.N,WindowKind.L,True,True,True,True),
 RelationDescriptor(RelationCode.NN,RelationFamily.PRIOR_N_CALENDAR_OFFSET,WindowKind.N,WindowKind.N,True,True,True,True),
 RelationDescriptor(RelationCode.WW,RelationFamily.WEEKLY_DEFERRED,WindowKind.W,WindowKind.W,False,False,True,False),
)
def registry_hash(): return canonical_sha256(CATALOG)
def resolve_relation(code):
    for item in CATALOG:
        if item.relation is code:return item
    raise FPI06Error('FP_HRC_RELATION_UNKNOWN','unknown relation',{'relation':str(code)})
def supported_relations():return tuple(item for item in CATALOG if item.supported_in_phase)
def validate_registry():
    if len({d.relation for d in CATALOG})!=7: raise FPI06Error('FP_HRC_RELATION_REGISTRY_DUPLICATE','relation registry duplicate')
    if tuple(d.relation.value for d in supported_relations())!=("AL","AN","LN","NA","NL","NN"): raise FPI06Error('FP_HRC_RELATION_ORDER_INVALID','supported relation order invalid')
    return True
