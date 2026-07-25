from __future__ import annotations
from decimal import Decimal
from .atom_base import AtomBase
from .descriptor_factory import descriptor
from .enums import TreatmentKind,ParameterType
from .parameters import ParameterSpec,ParameterSchema
from .plans import ManagementPlan,ManagementRule
D=Decimal
def S(a,*x): return ParameterSchema(f'{a}.params','1.0.0',tuple(x))
def P(n,t,d,mi=None,ma=None,u='unitless',allowed_values=()): return ParameterSpec(n,t,d,mi,ma,allowed_values=allowed_values,units=u)
class PartialExitAtR(AtomBase):
 descriptor=descriptor('management.partial_exit_r',TreatmentKind.MANAGEMENT,'partial_exit',S('management.partial_exit_r',P('activation_r',ParameterType.DECIMAL,'1','0','100','R'),P('quantity_fraction',ParameterType.DECIMAL,'0.5','0.01','1','fraction')))
 def build(self,c,i): return ManagementPlan(i.invocation_id,(ManagementRule('partial_exit_at_r',i.parameters.get_decimal('activation_r'),i.parameters.get_decimal('quantity_fraction')),))
class ScaleOutLadder(AtomBase):
 descriptor=descriptor('management.scale_out_ladder',TreatmentKind.MANAGEMENT,'scale_out',S('management.scale_out_ladder',P('first_r',ParameterType.DECIMAL,'1','0','100','R'),P('step_r',ParameterType.DECIMAL,'1','0.01','100','R'),P('leg_count',ParameterType.INTEGER,3,2,8,'count')))
 def build(self,c,i):
  n=i.parameters.get_int('leg_count'); f=D(1)/D(n); return ManagementPlan(i.invocation_id,tuple(ManagementRule('scale_out',i.parameters.get_decimal('first_r')+D(k)*i.parameters.get_decimal('step_r'),f) for k in range(n)))
class EvidenceAddOn(AtomBase):
 descriptor=descriptor('management.evidence_add_on',TreatmentKind.MANAGEMENT,'add_on',S('management.evidence_add_on',P('minimum_confidence',ParameterType.DECIMAL,'0.75','0','1','probability'),P('quantity_fraction',ParameterType.DECIMAL,'0.25','0.01','1','fraction')))
 def build(self,c,i): return ManagementPlan(i.invocation_id,(ManagementRule('add_on_when_confidence',i.parameters.get_decimal('minimum_confidence'),i.parameters.get_decimal('quantity_fraction')),),{'requires_fresh_risk_reservation':'true'})
class CancelRemaining(AtomBase):
 descriptor=descriptor('management.cancel_remaining',TreatmentKind.MANAGEMENT,'cancel_remaining',S('management.cancel_remaining',P('after_fill_fraction',ParameterType.DECIMAL,'0.5','0','1','fraction')))
 def build(self,c,i): return ManagementPlan(i.invocation_id,(ManagementRule('cancel_remaining_entries',i.parameters.get_decimal('after_fill_fraction'),D(0)),))
class MaximumHoldingTime(AtomBase):
 descriptor=descriptor('management.max_holding_time',TreatmentKind.MANAGEMENT,'time_exit',S('management.max_holding_time',P('holding_ms',ParameterType.INTEGER,14400000,1,604800000,'milliseconds')))
 def build(self,c,i): return ManagementPlan(i.invocation_id,(ManagementRule('force_exit_after_ms',i.parameters.get_int('holding_ms'),D(1)),))
class SessionCloseExit(AtomBase):
 descriptor=descriptor('management.session_close',TreatmentKind.MANAGEMENT,'session_close',S('management.session_close',P('lead_ms',ParameterType.INTEGER,300000,0,86400000,'milliseconds')),required=('session_close_ms',))
 def build(self,c,i): return ManagementPlan(i.invocation_id,(ManagementRule('force_exit_at_time',c.session_close_ms-i.parameters.get_int('lead_ms'),D(1)),))
class MarketStateGuard(AtomBase):
 descriptor=descriptor('management.market_state_guard',TreatmentKind.MANAGEMENT,'guard',S('management.market_state_guard',P('max_spread_points',ParameterType.DECIMAL,'50','0','100000','points'),P('action',ParameterType.ENUM,'block_add',allowed_values=('block_add','reduce','flatten'))))
 def build(self,c,i): return ManagementPlan(i.invocation_id,(ManagementRule('spread_guard',i.parameters.get_decimal('max_spread_points'),D(1),i.parameters.get_str('action')),))
class ForcedFlatten(AtomBase):
 descriptor=descriptor('management.forced_flatten',TreatmentKind.MANAGEMENT,'forced_flatten',S('management.forced_flatten',P('trigger_tag',ParameterType.STRING,'operator_kill')))
 def build(self,c,i): return ManagementPlan(i.invocation_id,(ManagementRule('force_flatten_on_tag',i.parameters.get_str('trigger_tag'),D(1)),),{'safety_priority':'highest'})
MANAGEMENT_ATOMS=(PartialExitAtR,ScaleOutLadder,EvidenceAddOn,CancelRemaining,MaximumHoldingTime,SessionCloseExit,MarketStateGuard,ForcedFlatten)
