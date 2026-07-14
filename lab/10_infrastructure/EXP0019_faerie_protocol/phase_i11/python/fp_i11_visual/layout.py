from math import ceil
from .contracts import LayoutContext
from .constants import MIN_PIXEL_GAP
def price_per_pixel(ctx:LayoutContext): return (ctx.visible_high-ctx.visible_low)/ctx.chart_height_px
def lane_step(ctx:LayoutContext):
 raw=max(ctx.tick_size,price_per_pixel(ctx)*MIN_PIXEL_GAP)
 return ceil(raw/ctx.tick_size)*ctx.tick_size
def lane_price(base,slot,ctx,above=True): return base+(lane_step(ctx)*slot if above else -lane_step(ctx)*slot)
def assign_lanes(items,lane_count):
 ordered=sorted(items,key=lambda x:(getattr(x,'first_hunt_time',getattr(x,'time',0)),getattr(x,'signal_id',getattr(x,'hunt_id',''))))
 return {getattr(x,'signal_id',getattr(x,'hunt_id',str(i))):i%lane_count for i,x in enumerate(ordered)}
