from __future__ import annotations
import math
from .models import LatencyHistogramSnapshot, LatencySloPolicy

class FixedLatencyHistogram:
    def __init__(self,policy:LatencySloPolicy):
        self.policy=policy; self.counts=[0]*len(policy.bucket_edges_us); self.overflow=0
        self.total=0; self.sum_us=0; self.minimum=0; self.maximum=0
    def observe(self,value_us:int)->None:
        if value_us<0: raise ValueError("latency cannot be negative")
        self.total+=1; self.sum_us+=value_us
        self.minimum=value_us if self.total==1 else min(self.minimum,value_us); self.maximum=max(self.maximum,value_us)
        for i,edge in enumerate(self.policy.bucket_edges_us):
            if value_us<=edge: self.counts[i]+=1; return
        self.overflow+=1
    def percentile(self,q:float)->int:
        if self.total==0:return 0
        target=max(1,math.ceil(self.total*q))
        cumulative=0
        for edge,count in zip(self.policy.bucket_edges_us,self.counts):
            cumulative+=count
            if cumulative>=target:return edge
        return self.maximum
    def snapshot(self,known_time_ms:int)->LatencyHistogramSnapshot:
        p50=self.percentile(.50);p95=self.percentile(.95);p99=self.percentile(.99)
        sufficient=self.total>=self.policy.minimum_samples
        breached=sufficient and (p50>self.policy.p50_limit_us or p95>self.policy.p95_limit_us or p99>self.policy.p99_limit_us)
        return LatencyHistogramSnapshot(stage=self.policy.stage,policy_id=self.policy.policy_id,sample_count=self.total,bucket_edges_us=self.policy.bucket_edges_us,bucket_counts=tuple(self.counts),overflow_count=self.overflow,minimum_us=self.minimum,maximum_us=self.maximum,mean_us=(self.sum_us/self.total if self.total else 0.0),p50_us=p50,p95_us=p95,p99_us=p99,slo_breached=breached,snapshot_time_ms=known_time_ms)
