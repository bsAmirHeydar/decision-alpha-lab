from .models import ViewSpecification,ViewFeatureDefinition,InputBinding,StaticNormalizer,ViewAuthorityBoundary
from .enums import ViewKind,FeatureType,MissingnessPolicy,NormalizationKind,TransformKind,EvidenceRole
ROLES=tuple(EvidenceRole)
def _f(fid,ft,inputs,transform=TransformKind.IDENTITY,required=False,missing=MissingnessPolicy.MASK,stale=None,quality=0.0,normalizer=None,cats=(),minimum=None,maximum=None,vector_length=None,default=None,description=''):
    return ViewFeatureDefinition(fid,ft,tuple(InputBinding(a,n,p) for a,n,p in inputs),transform,required,missing,default,stale,quality,normalizer or StaticNormalizer(),tuple(cats),minimum,maximum,vector_length,description)
def _spec(name,kind,features,twin_id='twin_golden',required=True,minimum_support=.75,description='',deps=(),limitations=()):
    return ViewSpecification(name,'1.0.0',twin_id,kind,tuple(features),ROLES,required,minimum_support,ViewAuthorityBoundary(),description,tuple(deps),tuple(limitations))

def institutional_view_catalog(twin_id='twin_golden'):
    price=_spec('price_view',ViewKind.PRICE,[
      _f('bid',FeatureType.NUMBER,[('x','projection','bid')],required=True,missing=MissingnessPolicy.PROHIBIT,stale=5000,quality=.8,minimum=0),
      _f('ask',FeatureType.NUMBER,[('x','projection','ask')],required=True,missing=MissingnessPolicy.PROHIBIT,stale=5000,quality=.8,minimum=0),
      _f('mid',FeatureType.NUMBER,[('bid','projection','bid'),('ask','projection','ask')],TransformKind.MIDPOINT,True,MissingnessPolicy.PROHIBIT,5000,.8,minimum=0),
      _f('spread',FeatureType.NUMBER,[('bid','projection','bid'),('ask','projection','ask')],TransformKind.SPREAD,True,MissingnessPolicy.PROHIBIT,5000,.8,minimum=0),
      _f('last_trade',FeatureType.NUMBER,[('x','projection','last_trade_price')],stale=15000,quality=.7,minimum=0),
      _f('short_return',FeatureType.NUMBER,[('now','projection','last_trade_price'),('prev','projection','previous_trade_price')],TransformKind.LOG_RETURN,missing=MissingnessPolicy.MASK,stale=60000,quality=.7)],twin_id,True,.8,'Executable point-in-time price state')
    structure=_spec('structure_view',ViewKind.STRUCTURE,[
      _f('lifecycle_state',FeatureType.CATEGORY,[('x','twin','lifecycle_state')],required=True,missing=MissingnessPolicy.PROHIBIT,cats=('initialized','valid','invalidated','observing')),
      _f('twin_state',FeatureType.CATEGORY,[('x','twin','twin_state')],required=True,missing=MissingnessPolicy.PROHIBIT,cats=('observing','degraded','conflicted','quarantined','initialized')),
      _f('reference_touch_count',FeatureType.NUMBER,[('x','projection','reference_touch_count')],minimum=0),
      _f('context_fresh',FeatureType.BOOLEAN,[('x','twin','context_fresh')],required=True,missing=MissingnessPolicy.UNKNOWN),
      _f('support_score',FeatureType.NUMBER,[('x','twin','support_score')],required=True,missing=MissingnessPolicy.PROHIBIT,minimum=0,maximum=1)],twin_id,True,.8,'Canonical and derived structural state')
    time=_spec('time_view',ViewKind.TIME,[
      _f('hour_utc',FeatureType.NUMBER,[('x','static','hour_utc')],required=True,missing=MissingnessPolicy.PROHIBIT,minimum=0,maximum=23),
      _f('weekday_utc',FeatureType.NUMBER,[('x','static','weekday_utc')],required=True,missing=MissingnessPolicy.PROHIBIT,minimum=0,maximum=6),
      _f('seconds_since_context_start',FeatureType.NUMBER,[('x','twin','context_start_time')],TransformKind.AGE_SECONDS,required=True,missing=MissingnessPolicy.PROHIBIT,minimum=0),
      _f('seconds_since_last_event',FeatureType.NUMBER,[('x','projection','last_event_marker')],TransformKind.AGE_SECONDS,missing=MissingnessPolicy.MASK,minimum=0)],twin_id,True,.75,'Canonical UTC timing without timezone ambiguity')
    htf=_spec('higher_timeframe_view',ViewKind.HIGHER_TIMEFRAME,[
      _f('htf_alignment',FeatureType.NUMBER,[('x','twin','htf_alignment')],required=True,missing=MissingnessPolicy.UNKNOWN,minimum=-1,maximum=1),
      _f('htf_phase',FeatureType.CATEGORY,[('x','twin','htf_phase')],required=True,missing=MissingnessPolicy.UNKNOWN,cats=('bullish','bearish','neutral','transition')),
      _f('htf_fresh',FeatureType.BOOLEAN,[('x','twin','htf_fresh')],required=True,missing=MissingnessPolicy.UNKNOWN)],twin_id,True,1.0,'Higher-timeframe context projection')
    inter=_spec('intermarket_view',ViewKind.INTERMARKET,[
      _f('related_score',FeatureType.NUMBER,[('x','projection','related_symbol_score')],required=True,missing=MissingnessPolicy.UNKNOWN,stale=15000,quality=.7,minimum=-1,maximum=1),
      _f('related_age_seconds',FeatureType.NUMBER,[('x','projection','related_symbol_score')],TransformKind.AGE_SECONDS,required=True,missing=MissingnessPolicy.UNKNOWN,minimum=0),
      _f('cross_market_state',FeatureType.CATEGORY,[('x','static','cross_market_state')],missing=MissingnessPolicy.MASK,cats=('confirming','diverging','neutral','unknown'))],twin_id,True,.66,'Asynchronous related-market evidence',limitations=('No implicit forward fill.',))
    liq=_spec('liquidity_view',ViewKind.LIQUIDITY,[
      _f('spread',FeatureType.NUMBER,[('bid','projection','bid'),('ask','projection','ask')],TransformKind.SPREAD,True,MissingnessPolicy.PROHIBIT,5000,.8,minimum=0),
      _f('quote_rate',FeatureType.NUMBER,[('x','projection','quote_rate')],missing=MissingnessPolicy.MASK,minimum=0),
      _f('trade_rate',FeatureType.NUMBER,[('x','projection','trade_rate')],missing=MissingnessPolicy.MASK,minimum=0),
      _f('gap_count',FeatureType.NUMBER,[('x','projection','gap_count')],minimum=0),
      _f('liquidity_state',FeatureType.CATEGORY,[('x','static','liquidity_state')],required=True,missing=MissingnessPolicy.UNKNOWN,cats=('normal','thin','stressed','unknown'))],twin_id,True,.6,'Liquidity and observability state')
    session=_spec('session_view',ViewKind.SESSION,[
      _f('session_id',FeatureType.CATEGORY,[('x','static','session_id')],required=True,missing=MissingnessPolicy.PROHIBIT,cats=('asia','london','new_york','overlap','closed')),
      _f('session_open',FeatureType.BOOLEAN,[('x','static','session_open')],required=True,missing=MissingnessPolicy.PROHIBIT),
      _f('minutes_from_open',FeatureType.NUMBER,[('x','static','minutes_from_open')],required=True,missing=MissingnessPolicy.PROHIBIT,minimum=-1440,maximum=1440),
      _f('boundary_recent',FeatureType.BOOLEAN,[('x','projection','session_boundary_recent')],missing=MissingnessPolicy.MASK)],twin_id,True,.75,'Session state in canonical calendar')
    execution=_spec('execution_view',ViewKind.EXECUTION,[
      _f('spread_points',FeatureType.NUMBER,[('x','execution','spread_points')],required=True,missing=MissingnessPolicy.UNKNOWN,minimum=0),
      _f('estimated_slippage_points',FeatureType.NUMBER,[('x','execution','estimated_slippage_points')],required=True,missing=MissingnessPolicy.UNKNOWN,minimum=0),
      _f('latency_ms',FeatureType.NUMBER,[('x','execution','latency_ms')],missing=MissingnessPolicy.MASK,minimum=0),
      _f('broker_state',FeatureType.CATEGORY,[('x','execution','broker_state')],required=True,missing=MissingnessPolicy.UNKNOWN,cats=('normal','degraded','closed','unknown'))],twin_id,False,.5,'Read-only execution economics; no broker authority')
    ancestry=_spec('context_ancestry_view',ViewKind.CONTEXT_ANCESTRY,[
      _f('context_family',FeatureType.STRING,[('x','twin','context_family')],required=True,missing=MissingnessPolicy.PROHIBIT),
      _f('parent_context_id',FeatureType.STRING,[('x','twin','parent_context_id')],missing=MissingnessPolicy.EXPLICIT_DEFAULT,default='none'),
      _f('generation_depth',FeatureType.NUMBER,[('x','twin','generation_depth')],required=True,missing=MissingnessPolicy.PROHIBIT,minimum=0),
      _f('transition_path',FeatureType.VECTOR,[('x','twin','transition_code_1'),('y','twin','transition_code_2')],TransformKind.VECTOR,missing=MissingnessPolicy.MASK,vector_length=2)],twin_id,False,.5,'Context family and ancestry descriptors')
    treatment=_spec('treatment_descriptor_view',ViewKind.TREATMENT_DESCRIPTOR,[
      _f('descriptor_id',FeatureType.STRING,[('x','approved_treatment','descriptor_id')],required=True,missing=MissingnessPolicy.UNKNOWN),
      _f('payoff_profile',FeatureType.CATEGORY,[('x','approved_treatment','payoff_profile')],required=True,missing=MissingnessPolicy.UNKNOWN,cats=('P1','P2','P3','P4','P5')),
      _f('entry_mechanism',FeatureType.CATEGORY,[('x','approved_treatment','entry_mechanism')],required=True,missing=MissingnessPolicy.UNKNOWN,cats=('breakout','market','pullback_limit')),
      _f('path_dependent',FeatureType.BOOLEAN,[('x','approved_treatment','path_dependent')],required=True,missing=MissingnessPolicy.UNKNOWN)],twin_id,False,1.0,'Read-only externally approved descriptor; cannot invent or select treatment',limitations=('V4-06 remains authority for Treatment DSL.','No treatment selection.'))
    return (price,structure,time,htf,inter,liq,session,execution,ancestry,treatment)
