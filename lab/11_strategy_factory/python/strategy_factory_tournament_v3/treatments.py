from __future__ import annotations
from .contracts import TreatmentSpec,TreatmentUniverseFreeze
from .enums import TreatmentFamily

def default_treatment_universe(declared_at_ms:int,outcome_cut_ms:int)->TreatmentUniverseFreeze:
 rows=(
 TreatmentSpec('uce15.treatment.tight_convex','1.0.0',TreatmentFamily.TIGHT_CONVEX,{'stop_atr':0.6,'target_r':2.0},1.0,False,'market','fixed_target','capital.fixed_risk'),
 TreatmentSpec('uce15.treatment.wide_survival','1.0.0',TreatmentFamily.WIDE_SURVIVAL,{'stop_atr':1.8,'time_limit_bars':40},1.0,False,'market','survival','capital.fixed_risk'),
 TreatmentSpec('uce15.treatment.limit','1.0.0',TreatmentFamily.LIMIT,{'offset_atr':0.25,'expiry_bars':4},1.0,False,'limit','fixed_target','capital.fixed_risk'),
 TreatmentSpec('uce15.treatment.confirmation','1.0.0',TreatmentFamily.CONFIRMATION,{'confirmation_bars':2},1.0,True,'confirmed_market','fixed_target','capital.fixed_risk'),
 TreatmentSpec('uce15.treatment.fixed_target','1.0.0',TreatmentFamily.FIXED_TARGET,{'target_r':2.5},1.0,False,'market','fixed_target','capital.fixed_risk'),
 TreatmentSpec('uce15.treatment.runner','1.0.0',TreatmentFamily.RUNNER,{'breakeven_r':1.0},1.0,False,'market','runner','capital.fixed_risk'),
 TreatmentSpec('uce15.treatment.fixed_plus_trail','1.0.0',TreatmentFamily.FIXED_PLUS_TRAIL,{'fixed_r':1.5,'trail_atr':1.0},1.0,False,'market','fixed_plus_trail','capital.fixed_risk'),
 TreatmentSpec('uce15.treatment.partial_plus_runner','1.0.0',TreatmentFamily.PARTIAL_PLUS_RUNNER,{'partial_fraction':0.5,'partial_r':1.0},1.0,False,'market','partial_plus_runner','capital.fixed_risk'),
 TreatmentSpec('uce15.treatment.capital_policy','1.0.0',TreatmentFamily.CAPITAL_POLICY,{'risk_fraction':0.0025,'daily_loss_limit_r':3.0},1.0,False,'market','capital_guard','capital.portfolio_guard'))
 return TreatmentUniverseFreeze('uce15.treatment_universe','1.0.0',declared_at_ms,outcome_cut_ms,rows,True)

def treatment_ids(universe:TreatmentUniverseFreeze)->tuple[str,...]:return tuple(x.treatment_id for x in universe.treatments)
