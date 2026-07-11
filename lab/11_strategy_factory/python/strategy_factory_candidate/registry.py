from __future__ import annotations
from .enums import PolicyKind
from .hashing import stable_id
class PolicyRegistry:
    def __init__(self):self._policies={};self._compiled=False;self.registry_hash=""
    def register(self,policy):
        if self._compiled: raise RuntimeError("registry already compiled")
        d=policy.descriptor; key=(d.policy_id,d.version)
        if key in self._policies: raise ValueError("duplicate policy identity")
        self._policies[key]=policy
    def compile(self):
        kinds={p.descriptor.kind for p in self._policies.values()}
        if not {PolicyKind.ENTRY,PolicyKind.STOP,PolicyKind.EXIT}.issubset(kinds):raise ValueError("entry, stop and exit policies required")
        payload="".join(f"|{int(p.descriptor.kind)}|{p.descriptor.hash}" for _,p in sorted(self._policies.items()))
        self.registry_hash=stable_id("preg",payload);self._compiled=True;return self.registry_hash
    def resolve(self,policy_id,version):return self._policies.get((policy_id,version))
    @property
    def compiled(self):return self._compiled
    def count(self,kind):return sum(p.descriptor.kind==kind for p in self._policies.values())
