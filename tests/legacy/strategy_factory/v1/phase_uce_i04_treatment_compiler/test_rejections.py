import pytest
from strategy_factory_treatment_compiler_v3.golden import baseline_draft
from strategy_factory_treatment_compiler_v3.contracts import TreatmentDraft,AtomSelection
from strategy_factory_treatment_compiler_v3.compiler import TreatmentCompiler
from strategy_factory_treatment_compiler_v3.errors import CompilationError
from strategy_factory_treatments_v3.catalog import build_default_catalog
from strategy_factory_treatments_v3.fixtures import reference_context
from strategy_factory_treatments_v3.enums import TreatmentKind
def test_missing_required_role_rejected():
 d=baseline_draft(); d=TreatmentDraft(d.draft_name,d.side,d.runtime_mode,d.compiler_mode,tuple(x for x in d.selections if x.role is not TreatmentKind.STOP),d.intrabar_policy)
 with pytest.raises(CompilationError): TreatmentCompiler(build_default_catalog()).compile(d,reference_context())
def test_management_over_exit_rejected():
 d=baseline_draft(); sels=d.selections+(AtomSelection(TreatmentKind.MANAGEMENT,'management.partial_exit_r@1.0.0',{'activation_r':'1','quantity_fraction':'0.75'}),AtomSelection(TreatmentKind.MANAGEMENT,'management.partial_exit_r@1.0.0',{'activation_r':'2','quantity_fraction':'0.75'},'second'))
 d=TreatmentDraft('bad.exit',d.side,d.runtime_mode,d.compiler_mode,sels,d.intrabar_policy)
 with pytest.raises(CompilationError): TreatmentCompiler(build_default_catalog()).compile(d,reference_context())
