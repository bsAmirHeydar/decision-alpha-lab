from __future__ import annotations
from abc import ABC,abstractmethod
from typing import Mapping
from .contracts import TreatmentAtomDescriptor,TreatmentAtomInvocation
from .context import TreatmentBuildContext
from .errors import CompatibilityError
class AtomBase(ABC):
    descriptor:TreatmentAtomDescriptor
    def invoke(self,ctx:TreatmentBuildContext,parameters:Mapping|None=None,provenance:Mapping[str,str]|None=None):
        d=self.descriptor
        if ctx.side not in d.compatibility.supported_sides: raise CompatibilityError('unsupported_side','side unsupported')
        if ctx.runtime_mode not in d.compatibility.supported_modes: raise CompatibilityError('unsupported_mode','runtime mode unsupported')
        missing=set(d.compatibility.required_context_fields)-ctx.available_fields
        if missing: raise CompatibilityError('missing_context_fields','required context fields missing',{'missing':sorted(missing)})
        packet=d.parameter_schema.bind(parameters)
        inv=TreatmentAtomInvocation(d.definition_id,d.exact_key,ctx.context_occurrence_id,ctx.feature_frame_hash,ctx.side,ctx.decision_time_ms,packet,dict(provenance or {}))
        return inv,self.build(ctx,inv)
    @abstractmethod
    def build(self,ctx,inv): ...
