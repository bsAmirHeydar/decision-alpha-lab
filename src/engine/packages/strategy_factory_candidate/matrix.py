from __future__ import annotations
from .models import CandidateTemplate
from .hashing import stable_id
class CandidateMatrixPlan:
    def __init__(self,plan_id:str,version:str):self.plan_id=plan_id;self.version=version;self.templates=[];self.compiled=False;self.plan_hash=""
    def add(self,t:CandidateTemplate):
        if self.compiled:raise RuntimeError("matrix already compiled")
        if any(x.template_id==t.template_id and x.template_version==t.template_version for x in self.templates):raise ValueError("duplicate template")
        self.templates.append(t)
    def compile(self,registry):
        if not registry.compiled:raise ValueError("registry not compiled")
        for t in self.templates:
            for pid,ver in ((t.entry_policy_id,t.entry_policy_version),(t.stop_policy_id,t.stop_policy_version),(t.exit_policy_id,t.exit_policy_version)):
                if registry.resolve(pid,ver) is None:raise ValueError(f"unresolved policy {pid}@{ver}")
        self.templates.sort(key=lambda t:(t.priority,t.template_id))
        self.plan_hash=stable_id("cmat","|".join([self.plan_id,self.version,registry.registry_hash,*[t.hash for t in self.templates]]));self.compiled=True;return self.plan_hash
