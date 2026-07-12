from __future__ import annotations
import itertools
from collections import Counter
from strategy_factory_treatments_v3.enums import TreatmentKind
from .contracts import *
from .errors import MatrixBudgetError,CompilationError
from .utils import stable_id,seeded_sample
class TreatmentMatrixGenerator:
    def __init__(self,compiler): self.compiler=compiler
    def generate(self,spec:MatrixSpec,context):
        axes=sorted(spec.axes,key=lambda x:x.role.value)
        cardinality=1
        for a in axes: cardinality*=len(a.values)
        cardinality*=len(spec.intrabar_policies)
        combos=list(itertools.product(*(a.values for a in axes),spec.intrabar_policies))
        truncated=0
        if cardinality>spec.max_combinations:
            if spec.overflow_policy is MatrixOverflowPolicy.REJECT: raise MatrixBudgetError('matrix_budget_exceeded','declared matrix exceeds generation budget',{'cardinality':cardinality,'max':spec.max_combinations})
            if spec.overflow_policy is MatrixOverflowPolicy.TRUNCATE_DETERMINISTIC: truncated=cardinality-spec.max_combinations; combos=combos[:spec.max_combinations]
            else: truncated=cardinality-spec.max_combinations; combos=seeded_sample(combos,spec.max_combinations,spec.seed)
        compiled=[]; reject=Counter(); generated=0
        for row in combos:
            generated+=1; vals=row[:-1]; policy=row[-1]; sels=[]
            for axis,val in zip(axes,vals): sels.append(AtomSelection(axis.role,val.exact_key,val.parameters,val.alias))
            draft=TreatmentDraft(f'{spec.matrix_id}.row.{generated:08d}',spec.side,spec.runtime_mode,spec.compiler_mode,tuple(sels),policy,tags={**spec.tags,'matrix_definition_id':spec.definition_id})
            try:t,_=self.compiler.compile(draft,context); compiled.append(t)
            except CompilationError as e: reject[e.code]+=1
            if len(compiled)>=spec.max_compiled:
                truncated+=len(combos)-generated; break
        ids=tuple(t.treatment_id for t in compiled)
        result=MatrixResult(spec.definition_id,generated,len(ids),sum(reject.values()),truncated,ids,dict(reject),stable_id('uceorder',ids))
        return tuple(compiled),result
