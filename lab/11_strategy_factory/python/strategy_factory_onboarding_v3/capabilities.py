from __future__ import annotations
from dataclasses import asdict
from .contracts import CapabilityDeclaration,ContextSpecification
from .enums import CapabilityDecision
from .canonical import canonical_sha256
from .errors import OnboardingError
REQUIRED=('shared_treatment','shared_economics','shared_validation','shared_runtime','known_time','deterministic_replay')
FORBIDDEN=('order_send','broker_write','network_fetch','future_data')
def validate_capabilities(spec:ContextSpecification)->str:
    m={x.capability_id:x for x in spec.capabilities}
    missing=[x for x in REQUIRED if x not in m or m[x].decision is CapabilityDecision.DENY]
    forbidden=[x for x in FORBIDDEN if x in m and m[x].decision is CapabilityDecision.ALLOW]
    if missing:raise OnboardingError('missing_required_capability','required capabilities missing',{'missing':missing})
    if forbidden:raise OnboardingError('forbidden_capability','forbidden capability allowed',{'forbidden':forbidden})
    return canonical_sha256([asdict(m[k]) for k in sorted(m)])

def default_capabilities(extra:tuple[CapabilityDeclaration,...]=())->tuple[CapabilityDeclaration,...]:
    base=[CapabilityDeclaration(x,CapabilityDecision.ALLOW,'required shared path') for x in REQUIRED]
    base.extend(CapabilityDeclaration(x,CapabilityDecision.DENY,'outside context authority') for x in FORBIDDEN)
    by={x.capability_id:x for x in base}
    for item in extra:by[item.capability_id]=item
    return tuple(by[k] for k in sorted(by))
