import pytest
from strategy_factory_treatment_compiler_v3.golden import compile_golden,baseline_draft
from strategy_factory_treatment_compiler_v3.manual import ManualTreatmentCompiler
from strategy_factory_treatment_compiler_v3.compiler import TreatmentCompiler
from strategy_factory_treatment_compiler_v3.contracts import ManualTreatmentBundle,TreatmentDraft
from strategy_factory_treatment_compiler_v3.errors import ManualBundleError
from strategy_factory_treatments_v3.catalog import build_default_catalog
from strategy_factory_treatments_v3.fixtures import reference_context
def test_manual_exact_parity():
 t,_=compile_golden(); d=baseline_draft(); d=TreatmentDraft(d.draft_name,d.side,d.runtime_mode,d.compiler_mode,d.selections,d.intrabar_policy,pinned=True)
 b=ManualTreatmentBundle('manual.test','1.0.0','owner',d,t.treatment_id)
 mt,_=ManualTreatmentCompiler(TreatmentCompiler(build_default_catalog())).compile(b,reference_context()); assert mt.treatment_id==t.treatment_id
def test_manual_mismatch_fails_closed():
 d=baseline_draft(); d=TreatmentDraft(d.draft_name,d.side,d.runtime_mode,d.compiler_mode,d.selections,d.intrabar_policy,pinned=True)
 b=ManualTreatmentBundle('manual.test','1.0.0','owner',d,'wrong')
 with pytest.raises(ManualBundleError): ManualTreatmentCompiler(TreatmentCompiler(build_default_catalog())).compile(b,reference_context())
