from __future__ import annotations
from dataclasses import dataclass
from .canonical import require_id,require_hash,canonical_sha256,sorted_unique
from .enums import *
from .constants import *
from .errors import FPI11Error
@dataclass(frozen=True,slots=True)
class ProjectionConfig:
 instance_id:str; object_namespace:str; mode:VisualMode=VisualMode.STANDARD; history_days:int=30; max_objects:int=MAX_OBJECTS_DEFAULT; show_sessions:bool=True; show_references:bool=True; show_hunts:bool=True; show_candidates:bool=True; show_confirmed:bool=True; show_ww:bool=True; show_suppressed:bool=True; show_health:bool=True
 def __post_init__(self):
  require_id(self.instance_id,'instance_id')
  if not self.object_namespace.startswith(OBJECT_NAMESPACE_PREFIX): raise FPI11Error('FP_VIS_NAMESPACE_INVALID','namespace must be instance scoped')
  if not 1<=self.history_days<=MAX_HISTORY_DAYS: raise FPI11Error('FP_VIS_HISTORY_INVALID','history days outside policy')
  if not 100<=self.max_objects<=10000: raise FPI11Error('FP_VIS_OBJECT_LIMIT_INVALID','max objects outside policy')
 @property
 def config_hash(self): return canonical_sha256(self)
@dataclass(frozen=True,slots=True)
class Style:
 style_id:str; stroke:str; fill:str; width:int; line_style:str; opacity:int; font_size:int; z_order:int
 def __post_init__(self):
  require_id(self.style_id,'style_id')
  if not (1<=self.width<=5 and 0<=self.opacity<=255 and 6<=self.font_size<=24): raise FPI11Error('FP_VIS_STYLE_INVALID','style dimensions invalid')
 @property
 def style_hash(self): return canonical_sha256(self)
@dataclass(frozen=True,slots=True)
class Anchor:
 anchor_type:AnchorType; time1:int=0; price1:float=0.; time2:int=0; price2:float=0.; corner:int=0; x:int=0; y:int=0
 def __post_init__(self):
  if self.anchor_type in (AnchorType.TIME_PRICE,AnchorType.TIME_RANGE) and self.time1<0: raise FPI11Error('FP_VIS_ANCHOR_TIME_INVALID','time invalid')
  if self.anchor_type is AnchorType.TIME_RANGE and self.time2<=self.time1: raise FPI11Error('FP_VIS_ANCHOR_RANGE_INVALID','time range invalid')
 @property
 def anchor_hash(self): return canonical_sha256(self)
@dataclass(frozen=True,slots=True)
class VisualObjectSpec:
 object_id:str; semantic_id:str; kind:ObjectKind; layer:Layer; state:VisualState; anchor:Anchor; style:Style; text:str; tooltip:str; immutable:bool; semantic_hash:str; projection_hash:str; reason_codes:tuple[str,...]=()
 def __post_init__(self):
  require_id(self.object_id,'object_id'); require_id(self.semantic_id,'semantic_id'); require_hash(self.semantic_hash,'semantic_hash'); require_hash(self.projection_hash,'projection_hash')
  if self.reason_codes!=sorted_unique(self.reason_codes): raise FPI11Error('FP_VIS_REASONS_NONCANONICAL','reason codes must be sorted unique')
@dataclass(frozen=True,slots=True)
class WindowFact:
 window_id:str; kind:str; start:int; end:int; high:float; low:float; state:SemanticState; semantic_hash:str
@dataclass(frozen=True,slots=True)
class ReferenceFact:
 reference_id:str; symbol:str; side:str; price:float; start:int; end:int; state:SemanticState; semantic_hash:str
@dataclass(frozen=True,slots=True)
class HuntFact:
 hunt_id:str; symbol:str; side:str; time:int; price:float; role:str; semantic_hash:str
@dataclass(frozen=True,slots=True)
class SignalFact:
 signal_id:str; relation:str; direction:str; hunter_symbol:str; protected_symbol:str; first_hunt_time:int; confirmation_time:int; hunter_price:float; protected_price:float; state:SemanticState; disposition:SignalDisposition; semantic_hash:str; reason_codes:tuple[str,...]=()
@dataclass(frozen=True,slots=True)
class WWFact:
 context_id:str; direction:str; start:int; end:int; state:SemanticState; hunter_symbol:str; protected_symbol:str; semantic_hash:str
@dataclass(frozen=True,slots=True)
class HealthFact:
 health_id:str; state:str; text:str; generated_at:int; semantic_hash:str
@dataclass(frozen=True,slots=True)
class VisualSnapshot:
 snapshot_id:str; revision_id:str; generated_at:int; windows:tuple[WindowFact,...]=(); references:tuple[ReferenceFact,...]=(); hunts:tuple[HuntFact,...]=(); signals:tuple[SignalFact,...]=(); ww_contexts:tuple[WWFact,...]=(); health:HealthFact|None=None
 def __post_init__(self): require_id(self.snapshot_id,'snapshot_id'); require_id(self.revision_id,'revision_id')
 @property
 def snapshot_hash(self): return canonical_sha256(self)
@dataclass(frozen=True,slots=True)
class MutationRecord:
 mutation:Mutation; object_id:str; prior_hash:str; next_hash:str; reason_code:str
@dataclass(frozen=True,slots=True)
class DirtySet:
 creates:tuple[VisualObjectSpec,...]; updates:tuple[VisualObjectSpec,...]; deletes:tuple[str,...]; unchanged:tuple[str,...]; mutations:tuple[MutationRecord,...]; dirty_hash:str
@dataclass(frozen=True,slots=True)
class ObjectInventory:
 instance_id:str; objects:tuple[VisualObjectSpec,...]; inventory_hash:str
@dataclass(frozen=True,slots=True)
class LayoutContext:
 visible_low:float; visible_high:float; chart_height_px:int; tick_size:float; lane_count:int
 def __post_init__(self):
  if self.visible_high<=self.visible_low or self.chart_height_px<=0 or self.tick_size<=0 or not 1<=self.lane_count<=MAX_LANES: raise FPI11Error('FP_VIS_LAYOUT_INVALID','layout context invalid')
@dataclass(frozen=True,slots=True)
class ProjectionResult:
 projection_id:str; snapshot_hash:str; specs:tuple[VisualObjectSpec,...]; dirty_set:DirtySet; object_count:int; degraded:bool; reason_codes:tuple[str,...]; projection_hash:str
