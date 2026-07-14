from fp_i10_indicator.benchmark import benchmark_incremental

def test_incremental_benchmark(engine):
 r=benchmark_incremental(engine,engine.cursor.last_processed_m1+60000,iterations=100); assert r['avg_microseconds']<5000 and r['iterations']==100
