import pytest
from strategy_factory_treatment_compiler_v3.matrix import TreatmentMatrixGenerator
from strategy_factory_treatment_compiler_v3.compiler import TreatmentCompiler
from strategy_factory_treatment_compiler_v3.contracts import *
from strategy_factory_treatment_compiler_v3.enums import *
from strategy_factory_treatment_compiler_v3.errors import MatrixBudgetError
from strategy_factory_treatments_v3.catalog import build_default_catalog
from strategy_factory_treatments_v3.fixtures import reference_context
from strategy_factory_treatments_v3.enums import *
def spec(maxc=10,policy=MatrixOverflowPolicy.REJECT):
 A=MatrixAxis;V=MatrixAxisValue;K=TreatmentKind
 axes=(A(K.ENTRY,(V('entry.immediate_market@1.0.0',{'max_age_ms':2000}),V('entry.passive_limit@1.0.0',{'offset_points':'10','ttl_ms':300000}))),A(K.STOP,(V('stop.fixed_distance@1.0.0',{'distance_points':'100'}),)),A(K.TARGET,(V('target.fixed_r@1.0.0',{'reward_multiple':'2','risk_points':'100'}),)),A(K.TRAILING,(V('trailing.none@1.0.0',{}),)),A(K.MANAGEMENT,(V('management.max_holding_time@1.0.0',{'holding_ms':1000}),)),A(K.SIZING,(V('sizing.fixed_cash@1.0.0',{'cash_amount':'100'}),)))
 return MatrixSpec('test.matrix','1.0.0',TradeSide.LONG,RuntimeMode.RESEARCH,CompilerMode.AI_SEARCH,axes,max_combinations=maxc,overflow_policy=policy)
def test_matrix_is_deterministic_and_bounded():
 g=TreatmentMatrixGenerator(TreatmentCompiler(build_default_catalog())); a,r1=g.generate(spec(),reference_context()); b,r2=g.generate(spec(),reference_context()); assert r1==r2 and len(a)==2
def test_budget_rejection():
 with pytest.raises(MatrixBudgetError): TreatmentMatrixGenerator(TreatmentCompiler(build_default_catalog())).generate(spec(1),reference_context())
