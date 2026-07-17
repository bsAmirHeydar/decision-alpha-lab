from __future__ import annotations
from dataclasses import dataclass
import re
from .errors import ContractError

_SEMVER=re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?(?:\+([0-9A-Za-z.-]+))?$")

@dataclass(frozen=True, slots=True)
class Version:
    major:int
    minor:int
    patch:int
    prerelease:str|None=None
    build:str|None=None

    @classmethod
    def parse(cls, value:str)->"Version":
        m=_SEMVER.fullmatch(value)
        if not m: raise ContractError(f"invalid semantic version: {value}")
        return cls(int(m.group(1)),int(m.group(2)),int(m.group(3)),m.group(4),m.group(5))

    def precedence_key(self):
        # Build metadata is ignored. Stable versions sort after prereleases.
        return (self.major,self.minor,self.patch, 1 if self.prerelease is None else 0, self.prerelease or "")

    def __lt__(self, other):
        if not isinstance(other,Version): return NotImplemented
        return self.precedence_key()<other.precedence_key()

    def __str__(self):
        out=f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease: out+=f"-{self.prerelease}"
        if self.build: out+=f"+{self.build}"
        return out


def _cmp(version:Version, op:str, rhs:Version)->bool:
    if op=="==": return version.precedence_key()==rhs.precedence_key()
    if op==">=": return not version<rhs
    if op=="<=": return version<rhs or version.precedence_key()==rhs.precedence_key()
    if op==">": return rhs<version
    if op=="<": return version<rhs
    raise ContractError(f"unsupported comparator: {op}")


def satisfies(version:str|Version, constraint:str)->bool:
    v=Version.parse(version) if isinstance(version,str) else version
    c=constraint.strip()
    if c in {"","*","x","X"}: return True
    if c.startswith("^"):
        lo=Version.parse(c[1:])
        if lo.major>0: hi=Version(lo.major+1,0,0)
        elif lo.minor>0: hi=Version(0,lo.minor+1,0)
        else: hi=Version(0,0,lo.patch+1)
        return _cmp(v,">=",lo) and _cmp(v,"<",hi)
    if c.startswith("~"):
        lo=Version.parse(c[1:]); hi=Version(lo.major,lo.minor+1,0)
        return _cmp(v,">=",lo) and _cmp(v,"<",hi)
    if "x" in c.lower() or "*" in c:
        parts=c.replace("X","x").replace("*","x").split(".")
        vals=[v.major,v.minor,v.patch]
        return all(p=="x" or int(p)==vals[i] for i,p in enumerate(parts))
    if any(c.startswith(x) for x in (">=","<=","==",">","<")) or "," in c:
        for term in [x.strip() for x in c.split(",") if x.strip()]:
            m=re.fullmatch(r"(>=|<=|==|>|<)\s*(.+)",term)
            if not m or not _cmp(v,m.group(1),Version.parse(m.group(2))): return False
        return True
    return v.precedence_key()==Version.parse(c).precedence_key()


def highest_satisfying(versions:list[str], constraint:str)->str|None:
    candidates=[Version.parse(x) for x in versions if satisfies(x,constraint)]
    return str(max(candidates)) if candidates else None
