from time import perf_counter
from .filters import apply_filters
from .panel import build_panel

def benchmark(items,snapshot,cfg,loops=100):
 start=perf_counter()
 for _ in range(loops):
  fr=apply_filters(items,cfg.filters,snapshot.computed_hash);build_panel(snapshot,fr,cfg.panel,0)
 elapsed=perf_counter()-start
 return {'loops':loops,'items':len(items),'elapsed_seconds':elapsed,'per_loop_ms':elapsed*1000/loops}
