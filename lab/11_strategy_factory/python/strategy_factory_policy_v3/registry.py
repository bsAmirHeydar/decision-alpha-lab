from __future__ import annotations
from dataclasses import dataclass,asdict
from .enums import NodeKind,Authority
from .graph import AUTHORITY_BY_KIND
from .canonical import canonical_sha256
from .errors import PolicyError
@dataclass(frozen=True,slots=True)
class NodeDescriptor:
    node_kind:str; authority:str; deterministic:bool; may_abstain:bool; creates_occurrence:bool=False; runtime_authority:bool=False

def registry(): return tuple(NodeDescriptor(k.value,AUTHORITY_BY_KIND[k].value,True,k.name.startswith('MODEL') or k in (NodeKind.FALLBACK,NodeKind.PORTFOLIO_ALLOCATION),False,False) for k in NodeKind)
def registry_snapshot():
    items=[asdict(x) for x in registry()]; return {'version':'1.0.0','count':len(items),'items':items,'registry_hash':canonical_sha256(items)}
def require_node(kind):
    key=kind.value if isinstance(kind,NodeKind) else str(kind)
    for d in registry():
        if d.node_kind==key:return d
    raise PolicyError('unknown_node_kind',f'unknown node kind {key}')
