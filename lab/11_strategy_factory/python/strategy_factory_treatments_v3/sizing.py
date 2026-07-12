from __future__ import annotations
from decimal import Decimal
from .atom_base import AtomBase
from .descriptor_factory import descriptor
from .enums import TreatmentKind,ParameterType,SizingUnit
from .parameters import ParameterSpec,ParameterSchema
from .plans import SizingPlan
from .utils import require
D=Decimal
def S(a,*x): return ParameterSchema(f'{a}.params','1.0.0',tuple(x))
def P(n,t,d,mi=None,ma=None,u='unitless',allowed_values=()): return ParameterSpec(n,t,d,mi,ma,allowed_values=allowed_values,units=u)
class FixedCashRisk(AtomBase):
 descriptor=descriptor('sizing.fixed_cash',TreatmentKind.SIZING,'fixed_cash',S('sizing.fixed_cash',P('cash_amount',ParameterType.DECIMAL,'100','0','1000000000','account_currency')))
 def build(self,c,i): return SizingPlan(i.invocation_id,SizingUnit.CASH_RISK,i.parameters.get_decimal('cash_amount'),c.cash_risk_budget or None)
class EquityFractionRisk(AtomBase):
 descriptor=descriptor('sizing.equity_fraction',TreatmentKind.SIZING,'equity_fraction',S('sizing.equity_fraction',P('fraction',ParameterType.DECIMAL,'0.01','0','1','fraction')),required=('account_equity',))
 def build(self,c,i): return SizingPlan(i.invocation_id,SizingUnit.CASH_RISK,c.account_equity*i.parameters.get_decimal('fraction'),c.cash_risk_budget or None)
class FixedVolume(AtomBase):
 descriptor=descriptor('sizing.fixed_volume',TreatmentKind.SIZING,'fixed_volume',S('sizing.fixed_volume',P('volume',ParameterType.DECIMAL,'0.1','0','1000000','lots')))
 def build(self,c,i): return SizingPlan(i.invocation_id,SizingUnit.VOLUME,i.parameters.get_decimal('volume'),None)
class RiskTier(AtomBase):
 descriptor=descriptor('sizing.risk_tier',TreatmentKind.SIZING,'risk_tier',S('sizing.risk_tier',P('low_cash',ParameterType.DECIMAL,'50','0','1000000000','account_currency'),P('medium_cash',ParameterType.DECIMAL,'100','0','1000000000','account_currency'),P('high_cash',ParameterType.DECIMAL,'200','0','1000000000','account_currency'),P('medium_confidence',ParameterType.DECIMAL,'0.6','0','1','probability'),P('high_confidence',ParameterType.DECIMAL,'0.8','0','1','probability')))
 def build(self,c,i):
  x=i.parameters.get_decimal('high_cash') if c.confidence>=i.parameters.get_decimal('high_confidence') else i.parameters.get_decimal('medium_cash') if c.confidence>=i.parameters.get_decimal('medium_confidence') else i.parameters.get_decimal('low_cash'); return SizingPlan(i.invocation_id,SizingUnit.CASH_RISK,x,c.cash_risk_budget or None)
class CappedFractionalKelly(AtomBase):
 descriptor=descriptor('sizing.capped_fractional_kelly',TreatmentKind.SIZING,'kelly',S('sizing.capped_fractional_kelly',P('kelly_fraction',ParameterType.DECIMAL,'0.25','0','1','fraction'),P('maximum_equity_fraction',ParameterType.DECIMAL,'0.02','0','1','fraction')),required=('account_equity',))
 def build(self,c,i):
  p=c.confidence; b=max(c.expected_payoff,D('0.000001')); full=max(D(0),(b*p-(D(1)-p))/b); f=min(full*i.parameters.get_decimal('kelly_fraction'),i.parameters.get_decimal('maximum_equity_fraction')); return SizingPlan(i.invocation_id,SizingUnit.CASH_RISK,c.account_equity*f,c.cash_risk_budget or None,f)
class VolatilityTargetSizing(AtomBase):
 descriptor=descriptor('sizing.volatility_target',TreatmentKind.SIZING,'volatility_target',S('sizing.volatility_target',P('target_volatility',ParameterType.DECIMAL,'0.01','0','10','fraction'),P('base_cash',ParameterType.DECIMAL,'100','0','1000000000','account_currency')),required=('realized_volatility',))
 def build(self,c,i):
  rv=max(c.realized_volatility,D('0.000001')); scale=min(D(10),i.parameters.get_decimal('target_volatility')/rv); return SizingPlan(i.invocation_id,SizingUnit.CASH_RISK,i.parameters.get_decimal('base_cash')*scale,c.cash_risk_budget or None,scale)
class DrawdownScaling(AtomBase):
 descriptor=descriptor('sizing.drawdown_scaling',TreatmentKind.SIZING,'drawdown',S('sizing.drawdown_scaling',P('base_cash',ParameterType.DECIMAL,'100','0','1000000000','account_currency'),P('minimum_scale',ParameterType.DECIMAL,'0.1','0','1','fraction'),P('maximum_drawdown',ParameterType.DECIMAL,'0.2','0.0001','1','fraction')))
 def build(self,c,i):
  scale=max(i.parameters.get_decimal('minimum_scale'),D(1)-min(D(1),c.drawdown_fraction/i.parameters.get_decimal('maximum_drawdown'))); return SizingPlan(i.invocation_id,SizingUnit.CASH_RISK,i.parameters.get_decimal('base_cash')*scale,c.cash_risk_budget or None,scale)
class ConfidenceScaling(AtomBase):
 descriptor=descriptor('sizing.confidence_scaling',TreatmentKind.SIZING,'confidence',S('sizing.confidence_scaling',P('base_cash',ParameterType.DECIMAL,'100','0','1000000000','account_currency'),P('floor_confidence',ParameterType.DECIMAL,'0.5','0','1','probability'),P('ceiling_confidence',ParameterType.DECIMAL,'0.9','0','1','probability')))
 def build(self,c,i):
  lo=i.parameters.get_decimal('floor_confidence'); hi=i.parameters.get_decimal('ceiling_confidence'); require(hi>lo,'invalid_confidence_range','ceiling must exceed floor'); scale=max(D(0),min(D(1),(c.confidence-lo)/(hi-lo))); return SizingPlan(i.invocation_id,SizingUnit.CASH_RISK,i.parameters.get_decimal('base_cash')*scale,c.cash_risk_budget or None,scale)
class PortfolioBudgetSizing(AtomBase):
 descriptor=descriptor('sizing.portfolio_budget',TreatmentKind.SIZING,'portfolio_budget',S('sizing.portfolio_budget',P('share',ParameterType.DECIMAL,'0.1','0','1','fraction')),required=('portfolio_budget',))
 def build(self,c,i): return SizingPlan(i.invocation_id,SizingUnit.NORMALIZED_BUDGET,c.portfolio_budget*i.parameters.get_decimal('share'),c.portfolio_budget)
SIZING_ATOMS=(FixedCashRisk,EquityFractionRisk,FixedVolume,RiskTier,CappedFractionalKelly,VolatilityTargetSizing,DrawdownScaling,ConfidenceScaling,PortfolioBudgetSizing)
