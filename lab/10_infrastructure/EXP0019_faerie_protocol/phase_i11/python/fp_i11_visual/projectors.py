from .contracts import *
from .enums import *
from .identity import make_spec
from .styles import *
from .layout import assign_lanes,lane_price

def project_windows(snapshot,cfg):
 if not cfg.show_sessions:return []
 out=[]
 for f in snapshot.windows:
  if f.kind not in ('A','L','N','W'):continue
  k=ObjectKind.WEEK_BOX if f.kind=='W' else ObjectKind.SESSION_BOX
  out.append(make_spec(namespace=cfg.object_namespace,semantic_id=f.window_id,kind=k,layer=Layer.BACKGROUND if f.kind=='W' else Layer.SESSIONS,state=VisualState.VISIBLE,anchor=Anchor(AnchorType.TIME_RANGE,f.start,f.high,f.end,f.low),style=style_for_window(f.kind),text=f.kind,tooltip=f'{f.kind} {f.state.value}',immutable=f.state is SemanticState.COMPLETE,semantic_hash=f.semantic_hash))
 return out

def project_references(snapshot,cfg):
 if not cfg.show_references:return []
 out=[]
 for f in snapshot.references:
  state=VisualState.STALE if f.state in (SemanticState.CONSUMED,SemanticState.EXPIRED) else VisualState.VISIBLE
  line=make_spec(namespace=cfg.object_namespace,semantic_id=f.reference_id,kind=ObjectKind.REFERENCE_LINE,layer=Layer.REFERENCES,state=state,anchor=Anchor(AnchorType.TIME_RANGE,f.start,f.price,f.end,f.price),style=style_for_reference(f.side),text='',tooltip=f'{f.symbol} {f.side} {f.price}',immutable=f.state in (SemanticState.CONSUMED,SemanticState.EXPIRED),semantic_hash=f.semantic_hash)
  label=make_spec(namespace=cfg.object_namespace,semantic_id=f.reference_id+'-LBL',kind=ObjectKind.REFERENCE_LABEL,layer=Layer.REFERENCES,state=state,anchor=Anchor(AnchorType.TIME_PRICE,f.end,f.price),style=style_for_reference(f.side),text=f'{f.symbol} {f.side}',tooltip=line.tooltip,immutable=line.immutable,semantic_hash=f.semantic_hash)
  out.extend((line,label))
 return out

def project_hunts(snapshot,cfg,layout):
 if not cfg.show_hunts:return []
 lanes=assign_lanes(snapshot.hunts,layout.lane_count);out=[]
 for f in snapshot.hunts:
  slot=lanes[f.hunt_id]+1; p=lane_price(f.price,slot,layout,above=f.side=='HIGH')
  out.append(make_spec(namespace=cfg.object_namespace,semantic_id=f.hunt_id,kind=ObjectKind.HUNT_MARKER,layer=Layer.HUNTS,state=VisualState.VISIBLE,anchor=Anchor(AnchorType.TIME_PRICE,f.time,p),style=STYLES['HUNT'],text='H',tooltip=f'{f.role} {f.symbol} {f.side}',immutable=True,semantic_hash=f.semantic_hash))
  out.append(make_spec(namespace=cfg.object_namespace,semantic_id=f.hunt_id+'-ROLE',kind=ObjectKind.ROLE_BADGE,layer=Layer.HUNTS,state=VisualState.VISIBLE,anchor=Anchor(AnchorType.TIME_PRICE,f.time,p),style=STYLES['HUNT'],text=f.role[:1],tooltip=f.role,immutable=True,semantic_hash=f.semantic_hash))
 return out

def project_signals(snapshot,cfg,layout):
 out=[]; lanes=assign_lanes(snapshot.signals,layout.lane_count)
 for f in snapshot.signals:
  if f.state is SemanticState.CANDIDATE and not cfg.show_candidates:continue
  if f.state is SemanticState.CONFIRMED and not cfg.show_confirmed:continue
  if f.disposition in (SignalDisposition.SUPPRESSED_BY_WW,SignalDisposition.SUPPRESSED_BY_QUOTA) and not (cfg.show_suppressed or cfg.mode is VisualMode.AUDIT):continue
  kind=ObjectKind.CONFIRMED_SIGNAL if f.state is SemanticState.CONFIRMED else ObjectKind.INVALIDATION_MARKER if f.state is SemanticState.INVALIDATED else ObjectKind.CANDIDATE_SIGNAL
  style=style_for_signal(f.direction,f.state,f.disposition)
  p2=lane_price(f.protected_price,lanes[f.signal_id]+1,layout,above=f.direction=='BEARISH')
  immutable=f.state in (SemanticState.CONFIRMED,SemanticState.INVALIDATED)
  out.append(make_spec(namespace=cfg.object_namespace,semantic_id=f.signal_id,kind=kind,layer=Layer.SIGNALS,state=VisualState.VISIBLE,anchor=Anchor(AnchorType.TIME_RANGE,f.first_hunt_time,f.hunter_price,max(f.confirmation_time,f.first_hunt_time+60_000),p2),style=style,text=f'{f.relation} {f.direction[0]}',tooltip=f'{f.disposition.value} {f.hunter_symbol}->{f.protected_symbol}',immutable=immutable,semantic_hash=f.semantic_hash,reason_codes=f.reason_codes))
  if f.disposition in (SignalDisposition.SUPPRESSED_BY_WW,SignalDisposition.SUPPRESSED_BY_QUOTA):
   out.append(make_spec(namespace=cfg.object_namespace,semantic_id=f.signal_id+'-SUP',kind=ObjectKind.SUPPRESSION_OVERLAY,layer=Layer.SUPPRESSION,state=VisualState.VISIBLE,anchor=Anchor(AnchorType.TIME_PRICE,max(f.confirmation_time,f.first_hunt_time),p2),style=style,text='WW' if f.disposition is SignalDisposition.SUPPRESSED_BY_WW else 'Q',tooltip=f.disposition.value,immutable=True,semantic_hash=f.semantic_hash,reason_codes=f.reason_codes))
  if f.disposition is SignalDisposition.QUOTA_WINNER:
   out.append(make_spec(namespace=cfg.object_namespace,semantic_id=f.signal_id+'-WIN',kind=ObjectKind.QUOTA_WINNER_BADGE,layer=Layer.BADGES,state=VisualState.VISIBLE,anchor=Anchor(AnchorType.TIME_PRICE,max(f.confirmation_time,f.first_hunt_time),p2),style=STYLES['WINNER'],text='1ST',tooltip='pair-session winner',immutable=True,semantic_hash=f.semantic_hash))
 return out

def project_ww(snapshot,cfg):
 if not cfg.show_ww:return []
 out=[]
 for f in snapshot.ww_contexts:
  style=STYLES['WW_BULL' if f.direction=='BULLISH' else 'WW_BEAR']
  out.append(make_spec(namespace=cfg.object_namespace,semantic_id=f.context_id,kind=ObjectKind.WW_CONTEXT,layer=Layer.BACKGROUND,state=VisualState.VISIBLE if f.state is SemanticState.CONFIRMED else VisualState.STALE,anchor=Anchor(AnchorType.TIME_RANGE,f.start,1.,f.end,0.),style=style,text=f'WW {f.direction[0]}',tooltip=f'{f.hunter_symbol}->{f.protected_symbol} {f.state.value}',immutable=True,semantic_hash=f.semantic_hash))
 return out

def project_health(snapshot,cfg):
 if not cfg.show_health or snapshot.health is None:return []
 f=snapshot.health; key='HEALTH_READY' if f.state=='READY' else 'HEALTH_DEGRADED' if f.state=='DEGRADED' else 'HEALTH_BLOCKED'
 return [make_spec(namespace=cfg.object_namespace,semantic_id=f.health_id,kind=ObjectKind.HEALTH_BADGE,layer=Layer.HEALTH,state=VisualState.VISIBLE,anchor=Anchor(AnchorType.SCREEN_CORNER,corner=0,x=10,y=20),style=STYLES[key],text=f.text,tooltip=f.state,immutable=False,semantic_hash=f.semantic_hash)]

def project_all(snapshot,cfg,layout):
 specs=project_windows(snapshot,cfg)+project_references(snapshot,cfg)+project_hunts(snapshot,cfg,layout)+project_signals(snapshot,cfg,layout)+project_ww(snapshot,cfg)+project_health(snapshot,cfg)
 return tuple(sorted(specs,key=lambda x:(int(x.layer),x.object_id)))
