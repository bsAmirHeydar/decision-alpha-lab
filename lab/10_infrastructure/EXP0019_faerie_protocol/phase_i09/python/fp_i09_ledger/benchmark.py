from time import perf_counter

def benchmark_rank(contenders,rounds=200):
    start=perf_counter()
    for _ in range(rounds): sorted(contenders,key=lambda c:c.rank_key)
    return {"contenders":len(contenders),"rounds":rounds,"elapsed_ms":(perf_counter()-start)*1000.0}
