from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .contracts import RuntimeBundleManifest
from .errors import BundleValidationError

@dataclass(frozen=True,slots=True)
class I13PolicyRuntimeBridge:
    """Binds the exact UCE-I13 graph dependencies into the immutable I14 bundle.

    The bridge deliberately delegates policy semantics to the accepted I13 engine.
    It neither widens support nor reconstructs policy behavior from runtime scores.
    """
    manifest:RuntimeBundleManifest
    graph:Any
    manual_policy:Any
    fallback_policy:Any
    authority_matrix:Any
    admission:Any|None=None
    def validate(self)->None:
        spec=getattr(self.graph,'spec',None)
        if spec is None:raise BundleValidationError('missing_compiled_graph','I13 compiled graph is required')
        checks={
            'policy_graph_hash':getattr(spec,'graph_hash',None),
            'manual_policy_hash':getattr(self.manual_policy,'policy_hash',None),
            'fallback_policy_hash':getattr(self.fallback_policy,'policy_hash',None),
            'authority_matrix_hash':getattr(self.authority_matrix,'matrix_hash',None),
        }
        for field,actual in checks.items():
            expected=getattr(self.manifest,field)
            if actual!=expected:raise BundleValidationError('i13_dependency_hash_mismatch',f'{field} does not match immutable runtime bundle',{'expected':expected,'actual':actual})
        admission_hash=getattr(spec,'admission_hash',None)
        if admission_hash is not None and self.admission is not None and admission_hash!=getattr(self.admission,'admission_hash',None):raise BundleValidationError('i13_admission_hash_mismatch','compiled graph admission differs from supplied admission')
    def execute(self,occurrence,model_output=None,operator_override=None):
        self.validate()
        from strategy_factory_policy_v3.engine import execute_policy
        return execute_policy(self.graph,occurrence,self.manual_policy,self.fallback_policy,self.authority_matrix,admission=self.admission,model_output=model_output,operator_override=operator_override)
