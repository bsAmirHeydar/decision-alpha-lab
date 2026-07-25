from __future__ import annotations

def gamma_at(weights,index):
    if index<=0: return 0.0
    if index<=len(weights): return float(weights[index-1])
    return 0.0
