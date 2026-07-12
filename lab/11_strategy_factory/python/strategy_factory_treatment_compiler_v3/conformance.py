from __future__ import annotations
from decimal import Decimal
from strategy_factory_treatments_v3.catalog import build_default_catalog
from strategy_factory_treatments_v3.fixtures import reference_context
from strategy_factory_treatments_v3.enums import TradeSide,RuntimeMode,TreatmentKind
from .compiler import TreatmentCompiler
from .golden import compile_golden,run_golden_paths,baseline_draft,runner_draft
from .manual import ManualTreatmentCompiler
from .matrix import TreatmentMatrixGenerator
from .contracts import *
from .enums import *
from .errors import *

def run_conformance():
    checks={}
    long,_=compile_golden(TradeSide.LONG); short,_=compile_golden(TradeSide.SHORT)
    checks['long_short_distinct']=long.treatment_id!=short.treatment_id
    long2,_=compile_golden(TradeSide.LONG); checks['deterministic_identity']=long.treatment_id==long2.treatment_id
    _,paths=run_golden_paths(); checks['golden_paths_terminal']=all(v['state']=='closed' for v in paths.values())
    bd=baseline_draft(); bd=TreatmentDraft(bd.draft_name,bd.side,bd.runtime_mode,bd.compiler_mode,bd.selections,bd.intrabar_policy,pinned=True)
    bundle=ManualTreatmentBundle('manual.fixed_r','1.0.0','alpha_lab',bd,long.treatment_id,'golden parity')
    mt,_=ManualTreatmentCompiler(TreatmentCompiler(build_default_catalog())).compile(bundle,reference_context())
    checks['manual_exact_parity']=mt.treatment_id==long.treatment_id
    axes=(
      MatrixAxis(TreatmentKind.ENTRY,(MatrixAxisValue('entry.immediate_market@1.0.0',{'max_age_ms':2000}),MatrixAxisValue('entry.passive_limit@1.0.0',{'offset_points':'10','ttl_ms':300000}))),
      MatrixAxis(TreatmentKind.STOP,(MatrixAxisValue('stop.fixed_distance@1.0.0',{'distance_points':'100'}),)),
      MatrixAxis(TreatmentKind.TARGET,(MatrixAxisValue('target.fixed_r@1.0.0',{'reward_multiple':'2','risk_points':'100'}),)),
      MatrixAxis(TreatmentKind.TRAILING,(MatrixAxisValue('trailing.none@1.0.0',{}),)),
      MatrixAxis(TreatmentKind.MANAGEMENT,(MatrixAxisValue('management.max_holding_time@1.0.0',{'holding_ms':14400000}),)),
      MatrixAxis(TreatmentKind.SIZING,(MatrixAxisValue('sizing.fixed_cash@1.0.0',{'cash_amount':'100'}),)),
    )
    spec=MatrixSpec('conformance.matrix','1.0.0',TradeSide.LONG,RuntimeMode.RESEARCH,CompilerMode.AI_SEARCH,axes,max_combinations=10,max_compiled=10)
    ts,res=TreatmentMatrixGenerator(TreatmentCompiler(build_default_catalog())).generate(spec,reference_context())
    checks['matrix_bounded']=res.compiled_count==2 and res.generated_count==2
    checks['unique_treatment_ids']=len({t.treatment_id for t in ts})==len(ts)
    return {'passed':all(checks.values()),'checks':checks,'treatment_ids':[long.treatment_id,short.treatment_id], 'paths':paths,'matrix':res.to_dict()}
