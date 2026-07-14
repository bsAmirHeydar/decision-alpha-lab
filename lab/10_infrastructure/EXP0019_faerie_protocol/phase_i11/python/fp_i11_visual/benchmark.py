from time import perf_counter_ns
def benchmark(engine,snapshot,layout,iterations=100):
 t=perf_counter_ns()
 for _ in range(iterations):engine.project(snapshot,layout)
 return {'iterations':iterations,'total_us':(perf_counter_ns()-t)//1000,'object_count':engine.last_result.object_count,'unchanged':len(engine.last_result.dirty_set.unchanged)}
